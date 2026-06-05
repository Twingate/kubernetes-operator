# Gateway integration

The operator can manage Twingate **Gateways** and their **Certificate
Authorities** as Kubernetes resources, and bind `TwingateResource`s to a gateway
via `gatewayRef` (replacing the deprecated per-resource `proxy` field).

## CRDs

Three entities, each synced to the Twingate backend on reconcile:

- **`TwingateCertificateAuthority`** — registers an X509 CA's public certificate
  (read from a `kubernetes.io/tls` Secret's `ca.crt`) with Twingate. Clients use
  it to trust gateways the CA signs. The backend has no CA *update* mutation, so
  a rotated certificate is reconciled by re-creating the CA, not updating it in
  place. Only `type: X509` is supported today (SSH is a future addition).
- **`TwingateGateway`** — the proxy infrastructure serving many resources.
  References a `TwingateCertificateAuthority` via `x509CertificateAuthorityRef`.
  Its `remoteNetwork` comes from the operator's own settings.
- **`TwingateResource`** with `gatewayRef` — a Kubernetes resource bound to a
  gateway. Set exactly one of `proxy` (deprecated) or `gatewayRef`.

See [`examples/`](../examples/) for `certificate-authority.yaml`,
`gateway.yaml`, and `resource-with-gateway.yaml`.

## Service annotation contract

When the gateway Helm chart is deployed as a subchart of `twingate-operator`
with `gateway.twingate.managed: true`, its `templates/service.yaml` (owned by the
[gateway repo](https://github.com/Twingate/gateway)) must annotate the gateway
Service with:

| Annotation | Meaning |
| --- | --- |
| `gateway.twingate.com: "true"` | Trigger — the operator reconciles a `TwingateGateway` + `TwingateCertificateAuthority` derived from this Service. |
| `gateway.twingate.com/tlsSecret: <name>` | The `kubernetes.io/tls` Secret the CA's `ca.crt` is read from. |

The operator derives the gateway address from the Service (the cluster DNS name
for `ClusterIP`, the ingress IP/hostname for `LoadBalancer`, plus port `443`).
When `resource.twingate.com: "true"` is also present, it additionally creates the
in-cluster Kubernetes resource (`kubernetes.default.svc.cluster.local`) bound to
the gateway via `gatewayRef`, taking name/alias from the `resource.twingate.com/*`
annotations. While `gateway.twingate.com` is present, the legacy
`resource.twingate.com` handlers defer so they never fight over or delete the
gateway-managed resource.

The CA, Gateway and resource are owned by the Service (owner references), so
deleting the Service tears them all down.

## Migration (in place)

Adding `twingate.managed: true` to a deployment that already exposes its cluster
via the legacy proxy-based flow migrates the existing Kubernetes resource **in
place**: the operator finds the `TwingateResource` the Service owns, reuses its
Twingate `spec.id`, and rewrites it from `proxy` to `gatewayRef`. Because the
backend entity id is preserved, existing access grants (`TwingateResourceAccess`
edges) are retained — the resource is never deleted and recreated.

> [!WARNING]
> The inverse is also true: **removing** `gateway.twingate.com` /
> `twingate.managed` (or deleting the Service) deletes the gateway-managed
> `TwingateResource`, which **revokes its access grants**. Treat disabling a
> managed gateway as a destructive operation.
