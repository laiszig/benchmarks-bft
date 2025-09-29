#### Start experiment
`USER='laiszig' PWORD='clpwd08' ./scripts/miyuki/main.py -e experiment-m510 -p m510-f-1 --project bft-brain-clone single pbft --config analysis/myconfigs/config.pbft.yaml`
`./scripts/miyuki/main.py -e <exp_name> -p <profile> single <protocol> --config <path_to_your_config.yaml>`

#### Watch leader's live log
`ssh -t laiszig@ms1124.utah.cloudlab.us -i scripts/miyuki/id_cloudlab "tmux attach -t cloudlab:0"`

#### Nagivating tmux windows
`ctrl+b 0, ctrl+b 1`

#### Killing the leader process
`ssh laiszig@ms1144.utah.cloudlab.us -i scripts/miyuki/id_cloudlab`
- Command: `~/BFTBrain/scripts/kill_process_port.sh 9020`