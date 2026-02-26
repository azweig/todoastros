#!/bin/bash
curl -X POST http://172.18.0.16:5010/openai -H "Content-Type: application/json" -d '{"prompt": "Tell me about Aries", "max_tokens": 100}'
