Launch a RunPod pod using the Parameter Golf template.

Use the RunPod GraphQL API at `https://api.runpod.io/graphql?api_key=$RUNPOD_API_KEY` (read key from env, or ask user).

Target GPU: "NVIDIA RTX 4000 Ada Generation", cloudType: SECURE, templateId: "y5cejece4j" (Parameter Golf), containerDiskInGb: 40, startSsh: true.

If that GPU is unavailable (SUPPLY_CONSTRAINT), retry every 5 seconds up to 20 times. If still unavailable after 20 attempts, suggest alternatives under $0.26/hr secure from gpuTypes query.

On success, query the pod runtime for the public SSH port (tcp type, isIpPublic: true) and print the SSH command:
  ssh -i ~/.ssh/id_runpod root@<ip> -p <port>

Also print the pod ID for use with /pod-kill.
