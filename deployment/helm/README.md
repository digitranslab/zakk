# Dependency updates (when subchart versions are bumped)
* If updating subcharts, you need to run this before committing!
* cd charts/zakk
* helm dependency update .

# Local testing

## One time setup
* brew install kind
* Ensure you have no config at ~/.kube/config
* kind create cluster
* mv ~/.kube/config ~/.kube/kind-config

## Automated install and test with ct
* export KUBECONFIG=~/.kube/kind-config
* kubectl config use-context kind-kind
* from source root run the following. This does a very basic test against the web server
  * ct install --all --helm-extra-set-args="--set=nginx.enabled=false" --debug --config ct.yaml

## Output template to file and inspect
* cd charts/zakk
* helm template test-output . > test-output.yaml

## Test the entire cluster manually
* cd charts/zakk
* helm install zakk . -n zakk --set postgresql.primary.persistence.enabled=false
  * the postgres flag is to keep the storage ephemeral for testing. You probably don't want to set that in prod.
  * no flag for ephemeral vespa storage yet, might be good for testing
* kubectl -n zakk port-forward service/zakk-nginx 8080:80
  * this will forward the local port 8080 to the installed chart for you to run tests, etc.
* When you are finished
  * helm uninstall zakk -n zakk
  * Vespa leaves behind a PVC. Delete it if you are completely done.
    * k -n zakk get pvc
    * k -n zakk delete pvc vespa-storage-da-vespa-0
  * If you didn't disable Postgres persistence earlier, you may want to delete that PVC too.

## Resourcing
In the helm charts, we have resource suggestions for all Zakk-owned components. 
These are simply initial suggestions, and may need to be tuned for your specific use case.

Please talk to us in Slack if you have any questions!
