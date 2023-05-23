.PHONY : apply destroy apply-stroage destroy-storage apply-compute \
destroy-compute build-and-push build-image push-image up

apply : apply-storage apply-compute

destroy : destroy-storage destroy-compute

apply-storage :
	terraform -chdir=storage apply

destroy-storage :
	terraform -chdir=storage destroy

apply-compute :
	terraform -chdir=compute apply

destroy-compute :
	terraform -chdir=compute destroy

build-and-push : build-image push-image

build-image :
	./build.sh

push-image :
	docker push $(IMAGE_NAME)

up : apply-storage build-image push-image apply-compute
