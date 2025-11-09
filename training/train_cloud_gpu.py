#!/usr/bin/env python3
"""
QLoRA Fine-tuning of Mistral-7B on Cloud GPU
Optimized for RunPod, Lambda Labs, Google Colab Pro, or Modal
Requires: CUDA GPU with 24GB+ VRAM (A100, A6000, RTX 4090)
"""

import json
import os
import torch
from datasets import Dataset, load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from huggingface_hub import HfApi, create_repo
import wandb

# ============================================================================
# CONFIGURATION
# ============================================================================

# Model Configuration
MODEL_NAME = "mistralai/Mistral-7B-v0.1"
OUTPUT_DIR = "./crowelogic-pharma-mistral-7b"
HF_MODEL_NAME = "MichaelCrowe11/CroweLogic-Pharma-Mistral-7B"  # Your HuggingFace username

# Dataset Configuration
TRAIN_FILE = "/workspace/crowelogic_pharma_100k_train.jsonl"
VAL_FILE = "/workspace/crowelogic_pharma_100k_val.jsonl"

# QLoRA Configuration (4-bit quantization)
USE_4BIT = True
BNB_4BIT_COMPUTE_DTYPE = "float16"
BNB_4BIT_QUANT_TYPE = "nf4"
USE_NESTED_QUANT = True

# LoRA Configuration
LORA_R = 16  # Rank
LORA_ALPHA = 32  # Alpha (typically 2x rank)
LORA_DROPOUT = 0.05
TARGET_MODULES = [
    "q_proj",
    "k_proj",
    "v_proj",
    "o_proj",
    "gate_proj",
    "up_proj",
    "down_proj",
]

# Training Configuration
BATCH_SIZE = 4  # Per device (can increase on A100)
GRADIENT_ACCUMULATION = 4  # Effective batch = 16
MAX_SEQ_LENGTH = 512
LEARNING_RATE = 2e-4
NUM_EPOCHS = 3
WARMUP_RATIO = 0.03
WEIGHT_DECAY = 0.001

# Logging & Saving
LOGGING_STEPS = 10
SAVE_STEPS = 500
EVAL_STEPS = 500
SAVE_TOTAL_LIMIT = 3

# Optional: Weights & Biases logging
USE_WANDB = False  # Set to True if you want W&B logging
WANDB_PROJECT = "crowelogic-pharma-mistral"

# ============================================================================
# SETUP
# ============================================================================

def setup_wandb():
    """Initialize Weights & Biases if enabled"""
    if USE_WANDB:
        wandb.init(
            project=WANDB_PROJECT,
            name=f"mistral-7b-qlora-{NUM_EPOCHS}epochs",
            config={
                "model": MODEL_NAME,
                "lora_r": LORA_R,
                "lora_alpha": LORA_ALPHA,
                "batch_size": BATCH_SIZE,
                "gradient_accumulation": GRADIENT_ACCUMULATION,
                "learning_rate": LEARNING_RATE,
                "epochs": NUM_EPOCHS,
                "max_seq_length": MAX_SEQ_LENGTH,
            }
        )

def load_datasets(train_file, val_file, tokenizer):
    """Load and tokenize training and validation datasets"""
    print(f"\n{'='*70}")
    print("Loading datasets...")
    print(f"{'='*70}\n")

    # Load JSONL files
    train_data = []
    val_data = []

    with open(train_file, 'r') as f:
        for line in f:
            train_data.append(json.loads(line))

    with open(val_file, 'r') as f:
        for line in f:
            val_data.append(json.loads(line))

    print(f"✓ Loaded {len(train_data):,} training examples")
    print(f"✓ Loaded {len(val_data):,} validation examples")

    # Format for instruction tuning (Mistral format)
    def format_instruction(example):
        text = f"<s>[INST] {example['instruction']} [/INST] {example['response']}</s>"
        return {"text": text}

    # Create datasets
    train_dataset = Dataset.from_list(train_data)
    val_dataset = Dataset.from_list(val_data)

    train_dataset = train_dataset.map(format_instruction)
    val_dataset = val_dataset.map(format_instruction)

    # Tokenize
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=MAX_SEQ_LENGTH,
            padding="max_length",
        )

    print("\nTokenizing datasets...")
    train_dataset = train_dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=train_dataset.column_names,
        desc="Tokenizing training set"
    )

    val_dataset = val_dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=val_dataset.column_names,
        desc="Tokenizing validation set"
    )

    print(f"✓ Tokenization complete")
    return train_dataset, val_dataset

def setup_model_and_tokenizer():
    """Initialize model and tokenizer with QLoRA configuration"""
    print(f"\n{'='*70}")
    print("Setting up model and tokenizer...")
    print(f"{'='*70}\n")

    # Tokenizer
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # BitsAndBytes config for 4-bit quantization
    print("Configuring 4-bit quantization...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=USE_4BIT,
        bnb_4bit_quant_type=BNB_4BIT_QUANT_TYPE,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=USE_NESTED_QUANT,
    )

    # Load model
    print("Loading base model with 4-bit quantization...")
    print("  (This will download ~4GB and may take 2-5 minutes)")

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )

    # Prepare model for k-bit training
    model = prepare_model_for_kbit_training(model)

    # LoRA configuration
    print("\nConfiguring LoRA adapters...")
    lora_config = LoraConfig(
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        target_modules=TARGET_MODULES,
        lora_dropout=LORA_DROPOUT,
        bias="none",
        task_type="CAUSAL_LM",
    )

    # Add LoRA adapters
    model = get_peft_model(model, lora_config)

    # Print trainable parameters
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    all_params = sum(p.numel() for p in model.parameters())

    print(f"\n✓ Model configured")
    print(f"  Trainable params: {trainable_params:,} ({100 * trainable_params / all_params:.2f}%)")
    print(f"  All params: {all_params:,}")
    print(f"  Memory footprint: ~{trainable_params * 4 / 1024**3:.2f} GB")

    return model, tokenizer

def train():
    """Main training function"""
    print("="*70)
    print("QLoRA Fine-tuning: Mistral-7B for CroweLogic-Pharma")
    print("="*70)
    print(f"\nHardware: Cloud GPU (CUDA)")
    print(f"Technique: QLoRA (4-bit + LoRA)")
    print(f"Dataset: 100,000 pharmaceutical + Crowe Logic examples")
    print()

    # Check CUDA availability
    if not torch.cuda.is_available():
        print("❌ ERROR: CUDA not available. This script requires GPU.")
        print("   Please run on: RunPod, Lambda Labs, Google Colab Pro, or Modal")
        return False

    print(f"✓ CUDA available: {torch.cuda.get_device_name(0)}")
    print(f"✓ VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB\n")

    # Setup W&B if enabled
    if USE_WANDB:
        setup_wandb()

    # Setup model and tokenizer
    model, tokenizer = setup_model_and_tokenizer()

    # Load datasets
    train_dataset, val_dataset = load_datasets(TRAIN_FILE, VAL_FILE, tokenizer)

    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    # Training arguments
    print(f"\n{'='*70}")
    print("Configuring training parameters...")
    print(f"{'='*70}\n")

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRADIENT_ACCUMULATION,
        gradient_checkpointing=True,
        learning_rate=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY,
        warmup_ratio=WARMUP_RATIO,
        logging_steps=LOGGING_STEPS,
        evaluation_strategy="steps",
        eval_steps=EVAL_STEPS,
        save_strategy="steps",
        save_steps=SAVE_STEPS,
        save_total_limit=SAVE_TOTAL_LIMIT,
        fp16=True,
        bf16=False,
        max_grad_norm=0.3,
        lr_scheduler_type="cosine",
        optim="paged_adamw_32bit",
        report_to="wandb" if USE_WANDB else "none",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        dataloader_num_workers=4,
        remove_unused_columns=False,
        push_to_hub=False,  # We'll push manually after training
    )

    print(f"✓ Training configuration:")
    print(f"  Epochs: {NUM_EPOCHS}")
    print(f"  Batch size per device: {BATCH_SIZE}")
    print(f"  Gradient accumulation: {GRADIENT_ACCUMULATION}")
    print(f"  Effective batch size: {BATCH_SIZE * GRADIENT_ACCUMULATION}")
    print(f"  Learning rate: {LEARNING_RATE}")
    print(f"  Max sequence length: {MAX_SEQ_LENGTH}")
    print(f"  Warmup ratio: {WARMUP_RATIO}")

    # Calculate training steps
    total_steps = (len(train_dataset) // (BATCH_SIZE * GRADIENT_ACCUMULATION)) * NUM_EPOCHS
    print(f"  Total training steps: {total_steps:,}")
    print(f"  Estimated time on A100: {total_steps * 0.5 / 60:.1f} minutes")

    # Initialize trainer
    print("\nInitializing trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
    )

    # Start training
    print(f"\n{'='*70}")
    print("Starting training...")
    print(f"{'='*70}\n")

    try:
        # Train
        trainer.train()

        print(f"\n{'='*70}")
        print("Training completed successfully!")
        print(f"{'='*70}\n")

        # Save final model
        print(f"Saving final model to {OUTPUT_DIR}...")
        model.save_pretrained(OUTPUT_DIR)
        tokenizer.save_pretrained(OUTPUT_DIR)

        print(f"\n✓ Model saved locally to: {OUTPUT_DIR}")

        # Optionally push to Hugging Face Hub
        push_to_hub = input("\nPush model to Hugging Face Hub? (yes/no): ").lower()
        if push_to_hub == 'yes':
            print(f"\nPushing to Hugging Face Hub as {HF_MODEL_NAME}...")
            model.push_to_hub(HF_MODEL_NAME)
            tokenizer.push_to_hub(HF_MODEL_NAME)
            print(f"✓ Model pushed to: https://huggingface.co/{HF_MODEL_NAME}")

        return True

    except Exception as e:
        print(f"\n✗ Training failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Entry point"""
    success = train()

    if success:
        print(f"\n{'='*70}")
        print("Next steps:")
        print(f"{'='*70}")
        print("1. Download model from cloud to local machine")
        print("2. Convert to GGUF format for Ollama (optional)")
        print("3. Integrate into GitHub repo: crowelogic-pharma-model")
        print("4. Test with pharmaceutical queries")
        print()

        print("To use the model:")
        print("  from peft import PeftModel")
        print("  from transformers import AutoModelForCausalLM, AutoTokenizer")
        print(f"  ")
        print(f'  base_model = AutoModelForCausalLM.from_pretrained("{MODEL_NAME}")')
        print(f'  model = PeftModel.from_pretrained(base_model, "{OUTPUT_DIR}")')
        print(f'  tokenizer = AutoTokenizer.from_pretrained("{OUTPUT_DIR}")')
        print()
    else:
        print("\nTraining failed. Please review errors above.")

if __name__ == "__main__":
    main()
