#!/bin/bash
# Sincroniza /root/.openclaw/anchors/ al repo memoria en github
cd /root/memoria
cp /root/.openclaw/anchors/documents/*.md "archivos documentos Open claw/documents/" 2>/dev/null
cp /root/.openclaw/anchors/skills/*.md "archivos documentos Open claw/skills/" 2>/dev/null
cp /root/.openclaw/anchors/index.json "archivos documentos Open claw/anchors/index.json" 2>/dev/null
git add -A
git -c user.name="Max" -c user.email="maxbry123@gmail.com" commit -m "sync anchors $(date +%Y-%m-%d_%H:%M)" 2>/dev/null
GIT_SSH_COMMAND="ssh -i /root/.ssh/github_deploy -o StrictHostKeyChecking=no" git push origin main 2>/dev/null
