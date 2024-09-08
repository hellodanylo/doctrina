import aws_cdk.aws_ecr as ecr
import aws_cdk.aws_codebuild as cb
import aws_cdk.aws_codecommit as cc
import aws_cdk.aws_codepipeline as cp
import aws_cdk.aws_codepipeline_actions as cpa
import aws_cdk.aws_events as e
import aws_cdk.aws_events_targets as et
import aws_cdk.aws_iam as iam
from aws_cdk import Stack, Duration


class DoctrinaBuildStack(Stack):
    def __init__(self, 
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        git_repo = cc.Repository(
            self, "CodeCommitRepository",
            repository_name="doctrina"
        )

        ecr_doctrina = ecr.Repository(
            self, "ECRRepository", 
            repository_name="doctrina",
            lifecycle_rules=[
                ecr.LifecycleRule(
                    tag_status=ecr.TagStatus.UNTAGGED, 
                    max_image_age=Duration.days(3),
                    description="delete untagged images after 3 days",
                ),
            ]
        )

        ecr_humus = ecr.Repository.from_repository_name(self, "ECRRepositoryHumus", repository_name="humus")

        role = iam.Role(
            self, "Role", 
            role_name="doctrina-codebuild",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal(service="codepipeline.amazonaws.com"),
                iam.ServicePrincipal(service="codebuild.amazonaws.com"),
            ),
            managed_policies=[
                iam.ManagedPolicy.from_managed_policy_arn(self, arn, managed_policy_arn=arn)
                for arn in [
                    "arn:aws:iam::aws:policy/AWSCloudFormationFullAccess",
                    "arn:aws:iam::aws:policy/AWSCodeBuildAdminAccess",
                    "arn:aws:iam::aws:policy/AWSCodeCommitPowerUser",
                    "arn:aws:iam::aws:policy/AWSCodePipeline_FullAccess",
                    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess",
                    "arn:aws:iam::aws:policy/AmazonEC2FullAccess",
                    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
                    "arn:aws:iam::aws:policy/AmazonSSMFullAccess",
                    "arn:aws:iam::aws:policy/CloudWatchFullAccess",
                    "arn:aws:iam::aws:policy/IAMFullAccess",
                ]
            ]
        )

        project = cb.PipelineProject(
            self, 
            f'Build', 
            project_name=f'doctrina',
            environment=cb.BuildEnvironment(
                build_image=cb.LinuxBuildImage.STANDARD_6_0,
                compute_type=cb.ComputeType.MEDIUM,
                privileged=True
            ),
            role=role,  # type: ignore
            build_spec=cb.BuildSpec.from_source_filename("cdk/buildspec.yml"),
        )

        doctrina_source = cp.Artifact(artifact_name="doctrina")

        pipeline = cp.Pipeline(
            self, 'Pipeline',
            pipeline_name='doctrina',
            role=role,  # type: ignore
            stages=[
                cp.StageProps(stage_name="source", actions=[
                    cpa.CodeCommitSourceAction(
                        repository=git_repo,
                        code_build_clone_output=True,
                        trigger=cpa.CodeCommitTrigger.EVENTS,
                        action_name="doctrina",
                        output=doctrina_source,
                        branch='main',
                        role=role,  # type: ignore
                    )
                ]),
                cp.StageProps(stage_name="build-base", actions=[
                    cpa.CodeBuildAction(
                        action_name="base", 
                        input=doctrina_source, 
                        project=project,  # type: ignore
                        role=role,  # type: ignore
                        environment_variables={
                            "HUMUS_REPO": cb.BuildEnvironmentVariable(value=ecr_humus.repository_uri),
                            "DOCTRINA_REPO": cb.BuildEnvironmentVariable(value=ecr_doctrina.repository_uri),
                            "DOCTRINA_IMAGE": cb.BuildEnvironmentVariable(value="base"),
                        }
                    ) 
                ]),
                cp.StageProps(stage_name=f"build-downstream", actions=[
                    cpa.CodeBuildAction(
                        action_name=image, 
                        input=doctrina_source, 
                        project=project,  # type: ignore
                        environment_variables={
                            "HUMUS_REPO": cb.BuildEnvironmentVariable(value=ecr_humus.repository_uri),
                            "DOCTRINA_REPO": cb.BuildEnvironmentVariable(value=ecr_doctrina.repository_uri),
                            "DOCTRINA_IMAGE": cb.BuildEnvironmentVariable(value=image)
                        },
                        role=role,  # type: ignore
                    )
                    for image in ["torch", "tf2", "stats", "cv", "xgb"]
                ])
            ]
        )

        event_role = iam.Role(
            self, "RoleEvent", 
            role_name="doctrina-event",
            assumed_by=iam.ServicePrincipal("events.amazonaws.com")
        )

        e.Rule(
            self, "EventRuleHumus", 
            rule_name="humus-ecr-trigger-doctrina-build",
            event_pattern=e.EventPattern(
                source=["aws.ecr"],
                detail_type=["ECR Image Action"],
                detail={
                    "action-type": ["PUSH"],
                    "result": ["SUCCESS"],
                    "repository-name": [ecr_humus.repository_name],
                    "image-tag": ["user-latest"],
                }
            ),
            targets=[et.CodePipeline(
                pipeline=pipeline, 
                event_role=event_role  # type: ignore
            )]
        )
