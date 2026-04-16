Terminate a RunPod pod to stop billing.

Arguments: `$ARGUMENTS` should contain the pod ID. If not provided, query the RunPod API to list running pods and ask which to kill.

Use the RunPod GraphQL API at `https://api.runpod.io/graphql?api_key=$RUNPOD_API_KEY` (read key from env, or ask user).

Run mutation:
  podTerminate(input: { podId: "<pod_id>" })

Confirm termination by querying the pod status. Print confirmation with the pod ID that was terminated.
