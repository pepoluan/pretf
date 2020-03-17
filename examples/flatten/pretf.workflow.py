from pretf import workflow


def pretf_workflow(path):

    workflow.require_files("*.*.auto.tfvars")

    with workflow.mirror_files("modules"):

        return workflow.default()
