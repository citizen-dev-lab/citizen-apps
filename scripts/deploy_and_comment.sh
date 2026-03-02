#!/usr/bin/env bash
set -euo pipefail

IMAGE="${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_AR_REPO}/${_SERVICE}:${COMMIT_SHA}"
echo "IMAGE=${IMAGE}"

EXEC_NAME="$(gcloud workflows run "${_WORKFLOW}" \
  --location="${_REGION}" \
  --data="{\"region\":\"${_REGION}\",\"serviceName\":\"${_SERVICE}\",\"image\":\"${IMAGE}\"}" \
  --format="value(name)")"

if [ -z "${EXEC_NAME}" ]; then
  echo "ERROR: could not get execution name"
  exit 1
fi
echo "EXEC_NAME=${EXEC_NAME}"

RESULT=""
for i in $(seq 1 80); do
  STATE="$(gcloud workflows executions describe "${EXEC_NAME}" \
    --location="${_REGION}" \
    --format="value(state)")"

  if [ "${STATE}" = "SUCCEEDED" ]; then
    RESULT="$(gcloud workflows executions describe "${EXEC_NAME}" \
      --location="${_REGION}" \
      --format="value(result)")"
    break
  fi

  if [ "${STATE}" = "FAILED" ] || [ "${STATE}" = "CANCELLED" ]; then
    echo "Workflow failed: ${STATE}"
    gcloud workflows executions describe "${EXEC_NAME}" --location="${_REGION}" --format=json | cat
    exit 1
  fi

  sleep 3
done

if [ -z "${RESULT}" ]; then
  echo "ERROR: workflow result not found (timeout?)"
  exit 1
fi

URL="$(echo "${RESULT}" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("url",""))')"
echo "URL=${URL}"

# python が参照するので export（重要）
export URL IMAGE

PAYLOAD="$(python3 -c 'import json,os
service=os.environ.get("_SERVICE","")
region=os.environ.get("_REGION","")
url=os.environ.get("URL","")
image=os.environ.get("IMAGE","")
body = "✅ Deploy completed\\n\\n- service: {}\\n- region: {}\\n- url: {}\\n- image: {}\\n".format(service, region, url, image)
print(json.dumps({"body": body}))
')"

API="https://api.github.com/repos/${_GH_OWNER}/${_GH_REPO}/commits/${COMMIT_SHA}/comments"
echo "POST ${API}"

# HTTPコードとレスポンスを必ず表示、失敗時はビルドも失敗させる
RESP="$(mktemp)"
HTTP_CODE="$(curl -sS -o "${RESP}" -w "%{http_code}" -X POST \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -H "Accept: application/vnd.github+json" \
  "${API}" \
  -d "${PAYLOAD}")"

echo "GitHub API status: ${HTTP_CODE}"
cat "${RESP}" | cat

if [ "${HTTP_CODE}" -lt 200 ] || [ "${HTTP_CODE}" -ge 300 ]; then
  echo "ERROR: GitHub comment post failed"
  exit 1
fi

echo "Posted deploy URL to commit comment."
