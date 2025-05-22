"""Test specifically for the pod labels fix to ensure app.kubernetes.io labels work properly."""

import pytest
from kubernetes.client.models import V1Deployment

from app.crds import ConnectorSpec, TwingateConnectorCRD
from app.handlers.handlers_connectors import get_connector_deployment


def test_pod_labels_precedence():
    """Test that the pod labels are properly merged, with selector labels taking precedence."""
    # Create a mock connector CRD
    connector_spec = ConnectorSpec(
        name="test-connector",
        pod_labels={
            "app.kubernetes.io/name": "test",  # This should be overridden
            "app.kubernetes.io/instance": "test-instance",  # This should be overridden
            "app.kubernetes.io/part-of": "test-app",  # This should be preserved
        },
    )
    
    crd = TwingateConnectorCRD(
        api_version="twingate.com/v1beta",
        kind="TwingateConnector",
        metadata={
            "name": "test-connector",
            "namespace": "default",
            "uid": "test-uid",
        },
        spec=connector_spec,
    )
    
    # Generate deployment
    deployment = get_connector_deployment(crd, "https://test.twingate.com", "twingate/connector:latest")
    
    # Check that the deployment is a V1Deployment
    assert isinstance(deployment, V1Deployment)
    
    # Extract labels from pod template
    pod_labels = deployment.spec["template"]["metadata"]["labels"]
    
    # Extract selector labels
    selector_labels = deployment.spec["selector"]["matchLabels"]
    
    # Verify the precedence of labels
    assert pod_labels["app.kubernetes.io/name"] == "TwingateConnector"  # Should be from selector
    assert pod_labels["app.kubernetes.io/instance"] == "test-connector"  # Should be from selector
    assert pod_labels["app.kubernetes.io/part-of"] == "test-app"  # Should be preserved from user input
    
    # Verify that selector matches pod template labels
    assert selector_labels["app.kubernetes.io/name"] == pod_labels["app.kubernetes.io/name"]
    assert selector_labels["app.kubernetes.io/instance"] == pod_labels["app.kubernetes.io/instance"]