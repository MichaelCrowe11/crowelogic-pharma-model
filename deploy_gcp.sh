#!/bin/bash
# GCP Deployment Script
# Deploy 100 instances for batch generation

set -e

DEPLOYMENT_ID=20251110_045340
ZONE=us-east-1-a
MACHINE_TYPE=e2-standard-2


# Launch batch 0
echo 'Launching pharma-batch-20251110_045340-0...'
gcloud compute instances create pharma-batch-20251110_045340-0 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=0,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 1
echo 'Launching pharma-batch-20251110_045340-1...'
gcloud compute instances create pharma-batch-20251110_045340-1 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=1,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 2
echo 'Launching pharma-batch-20251110_045340-2...'
gcloud compute instances create pharma-batch-20251110_045340-2 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=2,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 3
echo 'Launching pharma-batch-20251110_045340-3...'
gcloud compute instances create pharma-batch-20251110_045340-3 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=3,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 4
echo 'Launching pharma-batch-20251110_045340-4...'
gcloud compute instances create pharma-batch-20251110_045340-4 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=4,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 5
echo 'Launching pharma-batch-20251110_045340-5...'
gcloud compute instances create pharma-batch-20251110_045340-5 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=5,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 6
echo 'Launching pharma-batch-20251110_045340-6...'
gcloud compute instances create pharma-batch-20251110_045340-6 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=6,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 7
echo 'Launching pharma-batch-20251110_045340-7...'
gcloud compute instances create pharma-batch-20251110_045340-7 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=7,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 8
echo 'Launching pharma-batch-20251110_045340-8...'
gcloud compute instances create pharma-batch-20251110_045340-8 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=8,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 9
echo 'Launching pharma-batch-20251110_045340-9...'
gcloud compute instances create pharma-batch-20251110_045340-9 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=9,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 10
echo 'Launching pharma-batch-20251110_045340-10...'
gcloud compute instances create pharma-batch-20251110_045340-10 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=10,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 11
echo 'Launching pharma-batch-20251110_045340-11...'
gcloud compute instances create pharma-batch-20251110_045340-11 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=11,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 12
echo 'Launching pharma-batch-20251110_045340-12...'
gcloud compute instances create pharma-batch-20251110_045340-12 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=12,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 13
echo 'Launching pharma-batch-20251110_045340-13...'
gcloud compute instances create pharma-batch-20251110_045340-13 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=13,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 14
echo 'Launching pharma-batch-20251110_045340-14...'
gcloud compute instances create pharma-batch-20251110_045340-14 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=14,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 15
echo 'Launching pharma-batch-20251110_045340-15...'
gcloud compute instances create pharma-batch-20251110_045340-15 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=15,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 16
echo 'Launching pharma-batch-20251110_045340-16...'
gcloud compute instances create pharma-batch-20251110_045340-16 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=16,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 17
echo 'Launching pharma-batch-20251110_045340-17...'
gcloud compute instances create pharma-batch-20251110_045340-17 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=17,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 18
echo 'Launching pharma-batch-20251110_045340-18...'
gcloud compute instances create pharma-batch-20251110_045340-18 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=18,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 19
echo 'Launching pharma-batch-20251110_045340-19...'
gcloud compute instances create pharma-batch-20251110_045340-19 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=19,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 20
echo 'Launching pharma-batch-20251110_045340-20...'
gcloud compute instances create pharma-batch-20251110_045340-20 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=20,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 21
echo 'Launching pharma-batch-20251110_045340-21...'
gcloud compute instances create pharma-batch-20251110_045340-21 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=21,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 22
echo 'Launching pharma-batch-20251110_045340-22...'
gcloud compute instances create pharma-batch-20251110_045340-22 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=22,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 23
echo 'Launching pharma-batch-20251110_045340-23...'
gcloud compute instances create pharma-batch-20251110_045340-23 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=23,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 24
echo 'Launching pharma-batch-20251110_045340-24...'
gcloud compute instances create pharma-batch-20251110_045340-24 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=24,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 25
echo 'Launching pharma-batch-20251110_045340-25...'
gcloud compute instances create pharma-batch-20251110_045340-25 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=25,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 26
echo 'Launching pharma-batch-20251110_045340-26...'
gcloud compute instances create pharma-batch-20251110_045340-26 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=26,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 27
echo 'Launching pharma-batch-20251110_045340-27...'
gcloud compute instances create pharma-batch-20251110_045340-27 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=27,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 28
echo 'Launching pharma-batch-20251110_045340-28...'
gcloud compute instances create pharma-batch-20251110_045340-28 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=28,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 29
echo 'Launching pharma-batch-20251110_045340-29...'
gcloud compute instances create pharma-batch-20251110_045340-29 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=29,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 30
echo 'Launching pharma-batch-20251110_045340-30...'
gcloud compute instances create pharma-batch-20251110_045340-30 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=30,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 31
echo 'Launching pharma-batch-20251110_045340-31...'
gcloud compute instances create pharma-batch-20251110_045340-31 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=31,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 32
echo 'Launching pharma-batch-20251110_045340-32...'
gcloud compute instances create pharma-batch-20251110_045340-32 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=32,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 33
echo 'Launching pharma-batch-20251110_045340-33...'
gcloud compute instances create pharma-batch-20251110_045340-33 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=33,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 34
echo 'Launching pharma-batch-20251110_045340-34...'
gcloud compute instances create pharma-batch-20251110_045340-34 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=34,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 35
echo 'Launching pharma-batch-20251110_045340-35...'
gcloud compute instances create pharma-batch-20251110_045340-35 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=35,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 36
echo 'Launching pharma-batch-20251110_045340-36...'
gcloud compute instances create pharma-batch-20251110_045340-36 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=36,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 37
echo 'Launching pharma-batch-20251110_045340-37...'
gcloud compute instances create pharma-batch-20251110_045340-37 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=37,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 38
echo 'Launching pharma-batch-20251110_045340-38...'
gcloud compute instances create pharma-batch-20251110_045340-38 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=38,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 39
echo 'Launching pharma-batch-20251110_045340-39...'
gcloud compute instances create pharma-batch-20251110_045340-39 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=39,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 40
echo 'Launching pharma-batch-20251110_045340-40...'
gcloud compute instances create pharma-batch-20251110_045340-40 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=40,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 41
echo 'Launching pharma-batch-20251110_045340-41...'
gcloud compute instances create pharma-batch-20251110_045340-41 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=41,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 42
echo 'Launching pharma-batch-20251110_045340-42...'
gcloud compute instances create pharma-batch-20251110_045340-42 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=42,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 43
echo 'Launching pharma-batch-20251110_045340-43...'
gcloud compute instances create pharma-batch-20251110_045340-43 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=43,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 44
echo 'Launching pharma-batch-20251110_045340-44...'
gcloud compute instances create pharma-batch-20251110_045340-44 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=44,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 45
echo 'Launching pharma-batch-20251110_045340-45...'
gcloud compute instances create pharma-batch-20251110_045340-45 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=45,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 46
echo 'Launching pharma-batch-20251110_045340-46...'
gcloud compute instances create pharma-batch-20251110_045340-46 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=46,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 47
echo 'Launching pharma-batch-20251110_045340-47...'
gcloud compute instances create pharma-batch-20251110_045340-47 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=47,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 48
echo 'Launching pharma-batch-20251110_045340-48...'
gcloud compute instances create pharma-batch-20251110_045340-48 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=48,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 49
echo 'Launching pharma-batch-20251110_045340-49...'
gcloud compute instances create pharma-batch-20251110_045340-49 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=49,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 50
echo 'Launching pharma-batch-20251110_045340-50...'
gcloud compute instances create pharma-batch-20251110_045340-50 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=50,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 51
echo 'Launching pharma-batch-20251110_045340-51...'
gcloud compute instances create pharma-batch-20251110_045340-51 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=51,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 52
echo 'Launching pharma-batch-20251110_045340-52...'
gcloud compute instances create pharma-batch-20251110_045340-52 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=52,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 53
echo 'Launching pharma-batch-20251110_045340-53...'
gcloud compute instances create pharma-batch-20251110_045340-53 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=53,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 54
echo 'Launching pharma-batch-20251110_045340-54...'
gcloud compute instances create pharma-batch-20251110_045340-54 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=54,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 55
echo 'Launching pharma-batch-20251110_045340-55...'
gcloud compute instances create pharma-batch-20251110_045340-55 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=55,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 56
echo 'Launching pharma-batch-20251110_045340-56...'
gcloud compute instances create pharma-batch-20251110_045340-56 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=56,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 57
echo 'Launching pharma-batch-20251110_045340-57...'
gcloud compute instances create pharma-batch-20251110_045340-57 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=57,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 58
echo 'Launching pharma-batch-20251110_045340-58...'
gcloud compute instances create pharma-batch-20251110_045340-58 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=58,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 59
echo 'Launching pharma-batch-20251110_045340-59...'
gcloud compute instances create pharma-batch-20251110_045340-59 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=59,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 60
echo 'Launching pharma-batch-20251110_045340-60...'
gcloud compute instances create pharma-batch-20251110_045340-60 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=60,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 61
echo 'Launching pharma-batch-20251110_045340-61...'
gcloud compute instances create pharma-batch-20251110_045340-61 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=61,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 62
echo 'Launching pharma-batch-20251110_045340-62...'
gcloud compute instances create pharma-batch-20251110_045340-62 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=62,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 63
echo 'Launching pharma-batch-20251110_045340-63...'
gcloud compute instances create pharma-batch-20251110_045340-63 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=63,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 64
echo 'Launching pharma-batch-20251110_045340-64...'
gcloud compute instances create pharma-batch-20251110_045340-64 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=64,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 65
echo 'Launching pharma-batch-20251110_045340-65...'
gcloud compute instances create pharma-batch-20251110_045340-65 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=65,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 66
echo 'Launching pharma-batch-20251110_045340-66...'
gcloud compute instances create pharma-batch-20251110_045340-66 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=66,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 67
echo 'Launching pharma-batch-20251110_045340-67...'
gcloud compute instances create pharma-batch-20251110_045340-67 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=67,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 68
echo 'Launching pharma-batch-20251110_045340-68...'
gcloud compute instances create pharma-batch-20251110_045340-68 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=68,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 69
echo 'Launching pharma-batch-20251110_045340-69...'
gcloud compute instances create pharma-batch-20251110_045340-69 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=69,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 70
echo 'Launching pharma-batch-20251110_045340-70...'
gcloud compute instances create pharma-batch-20251110_045340-70 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=70,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 71
echo 'Launching pharma-batch-20251110_045340-71...'
gcloud compute instances create pharma-batch-20251110_045340-71 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=71,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 72
echo 'Launching pharma-batch-20251110_045340-72...'
gcloud compute instances create pharma-batch-20251110_045340-72 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=72,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 73
echo 'Launching pharma-batch-20251110_045340-73...'
gcloud compute instances create pharma-batch-20251110_045340-73 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=73,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 74
echo 'Launching pharma-batch-20251110_045340-74...'
gcloud compute instances create pharma-batch-20251110_045340-74 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=74,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 75
echo 'Launching pharma-batch-20251110_045340-75...'
gcloud compute instances create pharma-batch-20251110_045340-75 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=75,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 76
echo 'Launching pharma-batch-20251110_045340-76...'
gcloud compute instances create pharma-batch-20251110_045340-76 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=76,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 77
echo 'Launching pharma-batch-20251110_045340-77...'
gcloud compute instances create pharma-batch-20251110_045340-77 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=77,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 78
echo 'Launching pharma-batch-20251110_045340-78...'
gcloud compute instances create pharma-batch-20251110_045340-78 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=78,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 79
echo 'Launching pharma-batch-20251110_045340-79...'
gcloud compute instances create pharma-batch-20251110_045340-79 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=79,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 80
echo 'Launching pharma-batch-20251110_045340-80...'
gcloud compute instances create pharma-batch-20251110_045340-80 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=80,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 81
echo 'Launching pharma-batch-20251110_045340-81...'
gcloud compute instances create pharma-batch-20251110_045340-81 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=81,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 82
echo 'Launching pharma-batch-20251110_045340-82...'
gcloud compute instances create pharma-batch-20251110_045340-82 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=82,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 83
echo 'Launching pharma-batch-20251110_045340-83...'
gcloud compute instances create pharma-batch-20251110_045340-83 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=83,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 84
echo 'Launching pharma-batch-20251110_045340-84...'
gcloud compute instances create pharma-batch-20251110_045340-84 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=84,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 85
echo 'Launching pharma-batch-20251110_045340-85...'
gcloud compute instances create pharma-batch-20251110_045340-85 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=85,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 86
echo 'Launching pharma-batch-20251110_045340-86...'
gcloud compute instances create pharma-batch-20251110_045340-86 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=86,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 87
echo 'Launching pharma-batch-20251110_045340-87...'
gcloud compute instances create pharma-batch-20251110_045340-87 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=87,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 88
echo 'Launching pharma-batch-20251110_045340-88...'
gcloud compute instances create pharma-batch-20251110_045340-88 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=88,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 89
echo 'Launching pharma-batch-20251110_045340-89...'
gcloud compute instances create pharma-batch-20251110_045340-89 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=89,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 90
echo 'Launching pharma-batch-20251110_045340-90...'
gcloud compute instances create pharma-batch-20251110_045340-90 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=90,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 91
echo 'Launching pharma-batch-20251110_045340-91...'
gcloud compute instances create pharma-batch-20251110_045340-91 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=91,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 92
echo 'Launching pharma-batch-20251110_045340-92...'
gcloud compute instances create pharma-batch-20251110_045340-92 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=92,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 93
echo 'Launching pharma-batch-20251110_045340-93...'
gcloud compute instances create pharma-batch-20251110_045340-93 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=93,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 94
echo 'Launching pharma-batch-20251110_045340-94...'
gcloud compute instances create pharma-batch-20251110_045340-94 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=94,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 95
echo 'Launching pharma-batch-20251110_045340-95...'
gcloud compute instances create pharma-batch-20251110_045340-95 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=95,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 96
echo 'Launching pharma-batch-20251110_045340-96...'
gcloud compute instances create pharma-batch-20251110_045340-96 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=96,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 97
echo 'Launching pharma-batch-20251110_045340-97...'
gcloud compute instances create pharma-batch-20251110_045340-97 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=97,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 98
echo 'Launching pharma-batch-20251110_045340-98...'
gcloud compute instances create pharma-batch-20251110_045340-98 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=98,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

# Launch batch 99
echo 'Launching pharma-batch-20251110_045340-99...'
gcloud compute instances create pharma-batch-20251110_045340-99 \
  --zone=$ZONE \
  --machine-type=$MACHINE_TYPE \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=startup_script.sh \
  --labels=batch_id=99,deployment_id=$DEPLOYMENT_ID \
  --preemptible

sleep 2  # Rate limiting

echo 'Deployment complete!'
echo 'Monitor with: gcloud compute instances list --filter=labels.deployment_id=$DEPLOYMENT_ID'
