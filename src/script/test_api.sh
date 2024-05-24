#!/bin/bash

curl -w "\nTime: %{time_total}s\n" -X POST http://127.0.0.1:9001/id_allocation/allocation -d '{"graph_id":"cba9bbf5-ee77-48f6-919c-302fcd1c2a23","updated_nanosecond":1716482473640540,"vids":["twitter,chan_izaki65652","farcaster,gytred","ethereum,0x61ae970ac67ff4164ebf2fd6f38f630df522e5ef"]}'


curl -w "\nTime: %{time_total}s\n" -X POST 'http://ec2-18-167-19-252.ap-east-1.compute.amazonaws.com:9002/id_allocation/allocation' -d '{"graph_id":"101d4307-f84f-4942-b6ce-df0bab491bae","updated_nanosecond":1716565633694549,"vids":["crossbell,suji.csb","crossbell,sujiyan.csb","ethereum,0x934b510d4c9103e6a87aef13b816fb080286d649"]}'