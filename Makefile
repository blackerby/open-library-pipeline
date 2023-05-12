.PHONY : apply
apply : apply-storage apply-compute

.PHONY : destroy
destroy : destroy-storage destroy-compute

.PHONY : apply-storage
apply-storage :
	terraform -chdir=storage apply

.PHONY : destroy-storage
destroy-storage :
	terraform -chdir=storage destroy

.PHONY : apply-compute
apply-compute :
	terraform -chdir=compute apply

.PHONY : destroy-compute
destroy-compute :
	terraform -chdir=compute destroy

.PHONY : build-and-push
build-and-push : build-image push-image

.PHONY : build-image
build-image :
	./build.sh $(SCRIPT_NAME) $(FLOW_TAG) $(DEPLOYMENT_NAME) $(CRON)

.PHONY : push-image
push-image :
	docker push $(IMAGE_NAME)

.PHONY : delete-deployment
#currently broken
delete-deployment :
	prefect deployment delete $(DEPLOYMENT_NAME)

.PHONY : up
up : apply-storage build-image push-image apply-compute

.PHONY : down
# currently broken
down : delete-deployment destroy
