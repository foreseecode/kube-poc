### What we accomplished:
1) Monitoring, Logging, and reporting, Auto Deploy using argocd. see [tools](tools)
2) Auto deploy foresee applications to Kubernetes in namespace of dev and qal
Three apps can be deployed to kubernetes cluster:
    * [setting-service](https://github.com/foreseecode/settings-service/tree/poc/VOC-12275)
    * [fcp publisher](https://github.com/foreseecode/fcp-publisher/tree/poc/VOC-12275)
    * [event tracking service](https://github.com/foreseecode/event-tracking-service/tree/poc/VOC-12275)

### How does deployment work
After normal build we need to build and publish the docker images to our artifactory
```bash
cd service

mvn k8s:resource k8s:build k8s:push

_IMG=$(find target/classes/META-INF/jkube/kubernetes/*.yml | xargs fgrep image:)

if [ -z "$_IMG" ] ; then exit ; fi

APP_VERSION=`echo $_IMG | cut -d':' -f 4`
APP_NAME=`echo $_IMG | cut -d':' -f 3 | cut -d'/' -f 2`

if [ -z "$APP_VERSION" ] ; then exit ; fi
cd -
echo "APP_VERSION=$APP_VERSION" > deploy.props
echo "APP_NAME=$APP_NAME" >> deploy.props
echo "ENV=dev" >> deploy.props

cat deploy.props
```
Then use deploy.props to call another Jenkins job to update the [helm chart repo](./dev-qal)
see [Jenkins Job for Version Update](http://fsr-jenkins.aws.foreseeresults.com/job/Hierarchy/job/Kube_POC/job/version-updater/)

```
git checkout master

echo $APP_NAME $APP_VERSION
if [ -z "$APP_VERSION" ] ; then 
   exit
fi

cd dev-qal

array=(${ENV//,/ })

for i in "${!array[@]}"; do
  _env=${array[i]}
  FOLDER=$_env/$APP_NAME
  if [ -d "$FOLDER" ] ; then
    bash ./version_replace.sh $_env $APP_NAME $APP_VERSION
    git add $FOLDER
  fi
done

git commit -m "$ENV -> $APP_NAME to $APP_VERSION" || exit 0
git push -u origin master
```

Finally, the argoCD will watch the GitHub changes and deploy apps to Kubernetes. 

### How the helm chart is strucutred
#### Application Config
Currently dev-qal are shared same repo mimic the Dev/Qal environment.
1. [env file ](dev-qal/dev/env.yaml) which contains the generic configuration
2. for each enviroment, each apps has its own folder, for instance
[settings-service for dev](./dev-qal/dev/settings-service)
    * [version.conf](dev-qal/dev/settings-service/version.conf) which specified the app version and be update every deployment
    * [app.yaml](dev-qal/dev/settings-service/app.yaml) which is optional, for extra configuration

All logics are in [_help.yaml](dev-qal/templates/_help.yaml)
#### Security Config
In case of security configuration, we could have a different repo that stores it, demonstrated [here](dev-qal-secret)
We could have secrets in a private repo, defined with individual apps, e.g. [fcp publisher](dev-qal-secret/dev/fcp-publisher/secret.yaml)
and use a different argoCD project to deploy to the same namespace.

In the other word, for dev enviroment, we need have dev namespace inside Kubernetes, and there should be one argoCD project watches for new app deployment, and one argoCD project watches for secret changes or manually using helm for secret deployment.
