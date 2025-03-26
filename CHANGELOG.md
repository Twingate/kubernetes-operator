# CHANGELOG


## v0.18.0 (2025-03-26)

### Bug Fixes

- Support removing security policy from an access edge
  ([#583](https://github.com/Twingate/kubernetes-operator/pull/583),
  [`95a9932`](https://github.com/Twingate/kubernetes-operator/commit/95a99320db2f2470eb1ba8451f330aa7d93d7163))

## Related Tickets & Documents

- Issue: #581

## Changes

- When calling the update mutation if `securityPolicyId` is missing it means "dont change whats on
  server. We should send `null` when the object is missing one to use the default

### Chores

- Bump golang.org/x/net from 0.34.0 to 0.36.0
  ([#574](https://github.com/Twingate/kubernetes-operator/pull/574),
  [`540d508`](https://github.com/Twingate/kubernetes-operator/commit/540d508fc8230ee2d3e75cd12ad3691763137636))

Bumps [golang.org/x/net](https://github.com/golang/net) from 0.34.0 to 0.36.0. <details>
  <summary>Commits</summary> <ul> <li><a
  href="https://github.com/golang/net/commit/85d1d54551b68719346cb9fec24b911da4e452a1"><code>85d1d54</code></a>
  go.mod: update golang.org/x dependencies</li> <li><a
  href="https://github.com/golang/net/commit/cde1dda944dcf6350753df966bb5bda87a544842"><code>cde1dda</code></a>
  proxy, http/httpproxy: do not mismatch IPv6 zone ids against hosts</li> <li><a
  href="https://github.com/golang/net/commit/fe7f0391aa994a401c82d829183c1efab7a64df4"><code>fe7f039</code></a>
  publicsuffix: spruce up code gen and speed up PublicSuffix</li> <li><a
  href="https://github.com/golang/net/commit/459513d1f8abff01b4854c93ff0bff7e87985a0a"><code>459513d</code></a>
  internal/http3: move more common stream processing to genericConn</li> <li><a
  href="https://github.com/golang/net/commit/aad0180cad195ab7bcd14347e7ab51bece53f61d"><code>aad0180</code></a>
  http2: fix flakiness from t.Log when GOOS=js</li> <li><a
  href="https://github.com/golang/net/commit/b73e5746f64471c22097f07593643a743e7cfb0f"><code>b73e574</code></a>
  http2: don't log expected errors from writing invalid trailers</li> <li><a
  href="https://github.com/golang/net/commit/5f45c776a9c4d415cbe67d6c22c06fd704f8c9f1"><code>5f45c77</code></a>
  internal/http3: make read-data tests usable for server handlers</li> <li><a
  href="https://github.com/golang/net/commit/43c2540165a4d1bc9a81e06a86eb1e22ece64145"><code>43c2540</code></a>
  http2, internal/httpcommon: reject userinfo in :authority</li> <li><a
  href="https://github.com/golang/net/commit/1d78a085008d9fedfe3f303591058325f99727d7"><code>1d78a08</code></a>
  http2, internal/httpcommon: factor out server header logic for h2/h3</li> <li><a
  href="https://github.com/golang/net/commit/0d7dc54a591c12b4bd03bcd745024178d03d9218"><code>0d7dc54</code></a>
  quic: add Conn.ConnectionState</li> <li>Additional commits viewable in <a
  href="https://github.com/golang/net/compare/v0.34.0...v0.36.0">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=golang.org/x/net&package-manager=go_modules&previous-version=0.34.0&new-version=0.36.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself) You can disable automated security fix PRs for this repo from the
  [Security Alerts page](https://github.com/Twingate/kubernetes-operator/network/alerts).

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google-cloud-artifact-registry from 1.15.1 to 1.15.2
  ([#577](https://github.com/Twingate/kubernetes-operator/pull/577),
  [`33738c7`](https://github.com/Twingate/kubernetes-operator/commit/33738c77b080b8d2470ca51e930579d307cbdb68))

Bumps [google-cloud-artifact-registry](https://github.com/googleapis/google-cloud-python) from
  1.15.1 to 1.15.2. <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/googleapis/google-cloud-python/commit/5aeda454d1ecae0d301d9a4429155793f6508942"><code>5aeda45</code></a>
  chore: release main (<a

href="https://redirect.github.com/googleapis/google-cloud-python/issues/13644">#13644</a>)</li>
  <li><a
  href="https://github.com/googleapis/google-cloud-python/commit/c6a158821fad0f102d69b53781df3135c7483b31"><code>c6a1588</code></a>
  fix: set <code>include</code> in <code>tool.setuptools.packages.find</code> (<a
  href="https://redirect.github.com/googleapis/google-cloud-python/issues/13662">#13662</a>)</li>
  <li><a
  href="https://github.com/googleapis/google-cloud-python/commit/a2466af25d832eab04153e8bde446a9e9e523d2b"><code>a2466af</code></a>
  chore: remove google-cloud-resource-settings which is no longer being updated...</li> <li><a
  href="https://github.com/googleapis/google-cloud-python/commit/ae9565abe1003be49e335692d9f747a8a5de8b9b"><code>ae9565a</code></a>
  fix: resolve issue where pre-release versions of dependencies are installed (...</li> <li><a
  href="https://github.com/googleapis/google-cloud-python/commit/59bfd42cf8a2eaeed696a7504890bce5aae815ce"><code>59bfd42</code></a>
  fix: remove setup.cfg configuration for creating universal wheels (<a

href="https://redirect.github.com/googleapis/google-cloud-python/issues/13659">#13659</a>)</li>
  <li><a
  href="https://github.com/googleapis/google-cloud-python/commit/c7534a629586109f2680df8ece079b909e5978a7"><code>c7534a6</code></a>
  build: fix system test (<a

href="https://redirect.github.com/googleapis/google-cloud-python/issues/13658">#13658</a>)</li>
  <li><a
  href="https://github.com/googleapis/google-cloud-python/commit/8586a8fcc6cbe7a5cc18d3e30ae2a8914a2c61b3"><code>8586a8f</code></a>
  feat: [google-cloud-compute] Update Compute Engine API to revision 20250302 (...</li> <li><a
  href="https://github.com/googleapis/google-cloud-python/commit/9e302ca598ebc2eddd92b34633c40ba4750e9cfc"><code>9e302ca</code></a>
  feat: [google-shopping-merchant-datasources] Add a new destinations field (<a
  href="https://redirect.github.com/googleapis/google-cloud-python/issues/1">#1</a>...</li> <li><a
  href="https://github.com/googleapis/google-cloud-python/commit/de91574cdaeb557fcfce2dde03e633df96392012"><code>de91574</code></a>
  feat: [google-shopping-merchant-accounts] Add AutomaticImprovements service (...</li> <li><a
  href="https://github.com/googleapis/google-cloud-python/commit/daf198cd99ed710037b0120509af399aed3bcd25"><code>daf198c</code></a>
  docs: [google-cloud-eventarc-publishing] Minor documentation improvements (<a
  href="https://redirect.github.com/googleapis/google-cloud-python/issues/1">#1</a>...</li>
  <li>Additional commits viewable in <a
  href="https://github.com/googleapis/google-cloud-python/compare/google-cloud-artifact-registry-v1.15.1...google-cloud-artifact-registry-v1.15.2">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=google-cloud-artifact-registry&package-manager=pip&previous-version=1.15.1&new-version=1.15.2)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump gql from 3.5.1 to 3.5.2 ([#568](https://github.com/Twingate/kubernetes-operator/pull/568),
  [`d59d2c0`](https://github.com/Twingate/kubernetes-operator/commit/d59d2c0e2735823cf25e70e9b1c0fb56110aa414))

Bumps [gql](https://github.com/graphql-python/gql) from 3.5.1 to 3.5.2. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/graphql-python/gql/releases">gql's
  releases</a>.</em></p> <blockquote> <h2>v3.5.2</h2> <p>Now supporting graphql-core v3.2.4 again
  (See issue <a href="https://redirect.github.com/graphql-python/gql/issues/534">#534</a>)</p> <ul>
  <li>Allow graphql-core 3.2.4 by retrofitting introspection commits <a
  href="https://redirect.github.com/graphql-python/gql/issues/535">#535</a></li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/graphql-python/gql/commit/7881a9b3e594c4522927cc8a0f8f6bc2bb5d5989"><code>7881a9b</code></a>
  Bump version number to 3.5.2</li> <li><a
  href="https://github.com/graphql-python/gql/commit/ba70d2d79161b3c2417e3821cd9252728ed07ddb"><code>ba70d2d</code></a>
  Allow graphql-core 3.2.4 by retrofitting introspection commits (<a
  href="https://redirect.github.com/graphql-python/gql/issues/535">#535</a>)</li> <li>See full diff
  in <a href="https://github.com/graphql-python/gql/compare/v3.5.1...v3.5.2">compare view</a></li>
  </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=gql&package-manager=pip&previous-version=3.5.1&new-version=3.5.2)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump jinja2 from 3.1.5 to 3.1.6 ([#569](https://github.com/Twingate/kubernetes-operator/pull/569),
  [`4f40172`](https://github.com/Twingate/kubernetes-operator/commit/4f4017248d3994a1de8150a95258b8d66bc3787c))

Bumps [jinja2](https://github.com/pallets/jinja) from 3.1.5 to 3.1.6. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/pallets/jinja/releases">jinja2's
  releases</a>.</em></p> <blockquote> <h2>3.1.6</h2> <p>This is the Jinja 3.1.6 security release,
  which fixes security issues but does not otherwise change behavior and should not result in
  breaking changes compared to the latest feature release.</p> <p>PyPI: <a
  href="https://pypi.org/project/Jinja2/3.1.6/">https://pypi.org/project/Jinja2/3.1.6/</a> Changes:
  <a

href="https://jinja.palletsprojects.com/en/stable/changes/#version-3-1-6">https://jinja.palletsprojects.com/en/stable/changes/#version-3-1-6</a></p>
  <ul> <li>The <code>|attr</code> filter does not bypass the environment's attribute lookup,
  allowing the sandbox to apply its checks. <a
  href="https://github.com/pallets/jinja/security/advisories/GHSA-cpwx-vrp4-4pq7">https://github.com/pallets/jinja/security/advisories/GHSA-cpwx-vrp4-4pq7</a></li>
  </ul> </blockquote> </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/pallets/jinja/blob/main/CHANGES.rst">jinja2's changelog</a>.</em></p>
  <blockquote> <h2>Version 3.1.6</h2> <p>Released 2025-03-05</p> <ul> <li>The <code>|attr</code>
  filter does not bypass the environment's attribute lookup, allowing the sandbox to apply its
  checks. :ghsa:<code>cpwx-vrp4-4pq7</code></li> </ul> </blockquote> </details> <details>
  <summary>Commits</summary> <ul> <li><a
  href="https://github.com/pallets/jinja/commit/15206881c006c79667fe5154fe80c01c65410679"><code>1520688</code></a>
  release version 3.1.6</li> <li><a
  href="https://github.com/pallets/jinja/commit/90457bbf33b8662926ae65cdde4c4c32e756e403"><code>90457bb</code></a>
  Merge commit from fork</li> <li><a
  href="https://github.com/pallets/jinja/commit/065334d1ee5b7210e1a0a93c37238c86858f2af7"><code>065334d</code></a>
  attr filter uses env.getattr</li> <li><a
  href="https://github.com/pallets/jinja/commit/033c20015c7ca899ab52eb921bb0f08e6d3dd145"><code>033c200</code></a>
  start version 3.1.6</li> <li><a
  href="https://github.com/pallets/jinja/commit/bc68d4efa99c5f77334f0e519628558059ae8c35"><code>bc68d4e</code></a>
  use global contributing guide (<a
  href="https://redirect.github.com/pallets/jinja/issues/2070">#2070</a>)</li> <li><a
  href="https://github.com/pallets/jinja/commit/247de5e0c5062a792eb378e50e13e692885ee486"><code>247de5e</code></a>
  use global contributing guide</li> <li><a
  href="https://github.com/pallets/jinja/commit/ab8218c7a1b66b62e0ad6b941bd514e3a64a358f"><code>ab8218c</code></a>
  use project advisory link instead of global</li> <li><a
  href="https://github.com/pallets/jinja/commit/b4ffc8ff299dfd360064bea4cd2f862364601ad2"><code>b4ffc8f</code></a>
  release version 3.1.5 (<a
  href="https://redirect.github.com/pallets/jinja/issues/2066">#2066</a>)</li> <li>See full diff in
  <a href="https://github.com/pallets/jinja/compare/3.1.5...3.1.6">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=jinja2&package-manager=pip&previous-version=3.1.5&new-version=3.1.6)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself) You can disable automated security fix PRs for this repo from the
  [Security Alerts page](https://github.com/Twingate/kubernetes-operator/network/alerts).

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump kopf from 1.37.4 to 1.37.5 ([#586](https://github.com/Twingate/kubernetes-operator/pull/586),
  [`a827c42`](https://github.com/Twingate/kubernetes-operator/commit/a827c42c065918dcd0bd77b05d2df366801ab5a0))

Bumps [kopf](https://github.com/nolar/kopf) from 1.37.4 to 1.37.5. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/nolar/kopf/releases">kopf's
  releases</a>.</em></p> <blockquote> <h2>1.37.5</h2> <h2>What's Changed</h2> <ul> <li>Handle event
  refs with no apiVersion/kind fields at all by <a
  href="https://github.com/nolar"><code>@​nolar</code></a> in <a
  href="https://redirect.github.com/nolar/kopf/pull/1151">nolar/kopf#1151</a></li> <li>Add
  WebHookDockerDesktopServer by <a href="https://github.com/sgaist"><code>@​sgaist</code></a> in <a
  href="https://redirect.github.com/nolar/kopf/pull/1054">nolar/kopf#1054</a></li> </ul>
  <h2>Developer experience</h2> <ul> <li>Fix the numerous failures in CI: setuptools (python
  3.8/3.9), pre-commit, import-linter by <a href="https://github.com/nolar"><code>@​nolar</code></a>
  in <a href="https://redirect.github.com/nolar/kopf/pull/1160">nolar/kopf#1160</a></li> <li>Upgrade
  Ubuntu in CI (and pin oscrypto to an unreleased bugfix) by <a
  href="https://github.com/nolar"><code>@​nolar</code></a> in <a
  href="https://redirect.github.com/nolar/kopf/pull/1139">nolar/kopf#1139</a></li> <li>Switch to
  PyPI trusted publisher tokens by <a href="https://github.com/nolar"><code>@​nolar</code></a> in <a
  href="https://redirect.github.com/nolar/kopf/pull/1161">nolar/kopf#1161</a> <a
  href="https://redirect.github.com/nolar/kopf/pull/1162">nolar/kopf#1162</a></li> </ul> <h2>New
  Contributors</h2> <ul> <li><a href="https://github.com/sgaist"><code>@​sgaist</code></a> made
  their first contribution in <a
  href="https://redirect.github.com/nolar/kopf/pull/1054">nolar/kopf#1054</a></li> </ul>
  <p><strong>Full Changelog</strong>: <a
  href="https://github.com/nolar/kopf/compare/1.37.4...1.37.5">https://github.com/nolar/kopf/compare/1.37.4...1.37.5</a></p>
  </blockquote> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/nolar/kopf/commit/f2eba979998cdff627f812a517f56f74180779de"><code>f2eba97</code></a>
  Merge pull request <a href="https://redirect.github.com/nolar/kopf/issues/1162">#1162</a> from
  nolar/proper-trusted-publishing</li> <li><a
  href="https://github.com/nolar/kopf/commit/b769e9d60c8af9b93b1262547df7053f56da4080"><code>b769e9d</code></a>
  Put the GitHub Actions permissions into the proper place</li> <li><a
  href="https://github.com/nolar/kopf/commit/2df0431366da5bff68fc1f161c907a5b166a6eb1"><code>2df0431</code></a>
  Merge pull request <a href="https://redirect.github.com/nolar/kopf/issues/1054">#1054</a> from
  sgaist/dev_dockerdesktop</li> <li><a
  href="https://github.com/nolar/kopf/commit/caa8b60a6d74b86e35af70caa871b26ccd5e11c5"><code>caa8b60</code></a>
  Merge branch 'main' into dev_dockerdesktop</li> <li><a
  href="https://github.com/nolar/kopf/commit/c9f183428f683d8110ae9a1ed606e6dde07d7277"><code>c9f1834</code></a>
  Look for more specific alt-names in Docker Desktop certs</li> <li><a
  href="https://github.com/nolar/kopf/commit/dc2961b19be8c4f2584e70956838a0094dbbfe34"><code>dc2961b</code></a>
  Merge pull request <a href="https://redirect.github.com/nolar/kopf/issues/1151">#1151</a> from
  nolar/optional-apiversion-in-events</li> <li><a
  href="https://github.com/nolar/kopf/commit/51911fe02c5da668d40a706362db22025d04957b"><code>51911fe</code></a>
  Merge pull request <a href="https://redirect.github.com/nolar/kopf/issues/1161">#1161</a> from
  nolar/pypi-trusted-publisher</li> <li><a
  href="https://github.com/nolar/kopf/commit/b9256131e41c62c4e99153987802a2bdf0801d50"><code>b925613</code></a>
  Switch to PyPI trusted publisher tokens</li> <li><a
  href="https://github.com/nolar/kopf/commit/af6e882d4f859e954699077065978ea6607bd943"><code>af6e882</code></a>
  Merge pull request <a href="https://redirect.github.com/nolar/kopf/issues/1139">#1139</a> from
  nolar/upgrade-ubuntu</li> <li><a
  href="https://github.com/nolar/kopf/commit/d1fe513b9d60a30a67a5119012fd5f4148ea2d20"><code>d1fe513</code></a>
  Pin the oscrypto with the merged but unreleased hotfix for CI Ubuntu 24.04</li> <li>Additional
  commits viewable in <a href="https://github.com/nolar/kopf/compare/1.37.4...1.37.5">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=kopf&package-manager=pip&previous-version=1.37.4&new-version=1.37.5)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump multidict from 6.0.4 to 6.2.0
  ([`c2a23ef`](https://github.com/Twingate/kubernetes-operator/commit/c2a23efa65e91e4afd627a7bd62b795dca3c5d9d))

- Bump orjson from 3.10.15 to 3.10.16
  ([#587](https://github.com/Twingate/kubernetes-operator/pull/587),
  [`d4708cd`](https://github.com/Twingate/kubernetes-operator/commit/d4708cd1105fdc3d5164c2729a83d18e60c71369))

Bumps [orjson](https://github.com/ijl/orjson) from 3.10.15 to 3.10.16. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/ijl/orjson/releases">orjson's
  releases</a>.</em></p> <blockquote> <h2>3.10.16</h2> <h3>Changed</h3> <ul> <li>Improve performance
  of serialization on amd64 machines with AVX-512.</li> <li>ABI compatibility with CPython 3.14
  alpha 6.</li> <li>Drop support for Python 3.8.</li> <li>Publish additional PyPI wheels for macOS
  that target only aarch64, macOS 15, and recent Python.</li> </ul> </blockquote> </details>
  <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/ijl/orjson/blob/master/CHANGELOG.md">orjson's changelog</a>.</em></p>
  <blockquote> <h2>3.10.16</h2> <h3>Changed</h3> <ul> <li>Improve performance of serialization on
  amd64 machines with AVX-512.</li> <li>ABI compatibility with CPython 3.14 alpha 6.</li> <li>Drop
  support for Python 3.8.</li> <li>Publish additional PyPI wheels for macOS that target only
  aarch64, macOS 15, and recent Python.</li> </ul> </blockquote> </details> <details>
  <summary>Commits</summary> <ul> <li><a
  href="https://github.com/ijl/orjson/commit/1d8b3526a45ebfba7256289216aa4d36c6fc2e82"><code>1d8b352</code></a>
  3.10.16</li> <li><a
  href="https://github.com/ijl/orjson/commit/b0a91dfe459b44f98af585e928fbfe1cdd30329b"><code>b0a91df</code></a>
  Use function pointers for AVX-512 path</li> <li><a
  href="https://github.com/ijl/orjson/commit/56d6457fbff50247303100f3bc80b6999bbbc778"><code>56d6457</code></a>
  Fix various lints and set debug_asserts</li> <li><a
  href="https://github.com/ijl/orjson/commit/53d137ed20e658fe662d29d1f96fc58e12c16a05"><code>53d137e</code></a>
  pydict_setitem!()</li> <li><a
  href="https://github.com/ijl/orjson/commit/5ae468a084a9b44eda25fe4314b92cd679315c11"><code>5ae468a</code></a>
  ABI compatibility with CPython 3.14 PyASCIIObject.state</li> <li><a
  href="https://github.com/ijl/orjson/commit/5b2481d5ac349d6fbb956cd773c5fbf49766cbdc"><code>5b2481d</code></a>
  build maintenance, check-pypi, drop support for 3.8</li> <li>See full diff in <a
  href="https://github.com/ijl/orjson/compare/3.10.15...3.10.16">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=orjson&package-manager=pip&previous-version=3.10.15&new-version=3.10.16)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pre-commit from 4.1.0 to 4.2.0
  ([#580](https://github.com/Twingate/kubernetes-operator/pull/580),
  [`fba7e1d`](https://github.com/Twingate/kubernetes-operator/commit/fba7e1d59ecec5441b50d221afcb3a5f76c3b8a0))

Bumps [pre-commit](https://github.com/pre-commit/pre-commit) from 4.1.0 to 4.2.0. <details>
  <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/pre-commit/pre-commit/releases">pre-commit's releases</a>.</em></p>
  <blockquote> <h2>pre-commit v4.2.0</h2> <h3>Features</h3> <ul> <li>For <code>language:
  python</code> first attempt a versioned python executable for the default language version before
  consulting a potentially unversioned <code>sys.executable</code>. <ul> <li><a
  href="https://redirect.github.com/pre-commit/pre-commit/issues/3430">#3430</a> PR by <a
  href="https://github.com/asottile"><code>@​asottile</code></a>.</li> </ul> </li> </ul>
  <h3>Fixes</h3> <ul> <li>Handle error during conflict detection when a file is named
  &quot;HEAD&quot; <ul> <li><a
  href="https://redirect.github.com/pre-commit/pre-commit/issues/3425">#3425</a> PR by <a
  href="https://github.com/tusharsadhwani"><code>@​tusharsadhwani</code></a>.</li> </ul> </li> </ul>
  </blockquote> </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/pre-commit/pre-commit/blob/main/CHANGELOG.md">pre-commit's
  changelog</a>.</em></p> <blockquote> <h1>4.2.0 - 2025-03-18</h1> <h3>Features</h3> <ul> <li>For
  <code>language: python</code> first attempt a versioned python executable for the default language
  version before consulting a potentially unversioned <code>sys.executable</code>. <ul> <li><a
  href="https://redirect.github.com/pre-commit/pre-commit/issues/3430">#3430</a> PR by <a
  href="https://github.com/asottile"><code>@​asottile</code></a>.</li> </ul> </li> </ul>
  <h3>Fixes</h3> <ul> <li>Handle error during conflict detection when a file is named
  &quot;HEAD&quot; <ul> <li><a
  href="https://redirect.github.com/pre-commit/pre-commit/issues/3425">#3425</a> PR by <a
  href="https://github.com/tusharsadhwani"><code>@​tusharsadhwani</code></a>.</li> </ul> </li> </ul>
  </blockquote> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/pre-commit/pre-commit/commit/aa48766b888990e7b118d12cf757109d96e65a7e"><code>aa48766</code></a>
  v4.2.0</li> <li><a
  href="https://github.com/pre-commit/pre-commit/commit/bf6f11dc6ce59f2f12e5d02a6449ea2449aa64c4"><code>bf6f11d</code></a>
  Merge pull request <a
  href="https://redirect.github.com/pre-commit/pre-commit/issues/3430">#3430</a> from
  pre-commit/preferential-sys-impl</li> <li><a
  href="https://github.com/pre-commit/pre-commit/commit/3e8d0f5e1c449381272b80241140e985631f9912"><code>3e8d0f5</code></a>
  adjust python default_language_version to prefer versioned exe</li> <li><a
  href="https://github.com/pre-commit/pre-commit/commit/ff7256cedf8c78b326f4503373d142a5a9827e90"><code>ff7256c</code></a>
  Merge pull request <a
  href="https://redirect.github.com/pre-commit/pre-commit/issues/3425">#3425</a> from
  tusharsadhwani/ambiguous-ref</li> <li><a
  href="https://github.com/pre-commit/pre-commit/commit/b7eb412c798424a94ca83c72eed6f97271545dc4"><code>b7eb412</code></a>
  fix: crash on ambiguous ref 'HEAD'</li> <li><a
  href="https://github.com/pre-commit/pre-commit/commit/7b88c63ae691cb243c3137bce8fb870523e0a884"><code>7b88c63</code></a>
  Merge pull request <a
  href="https://redirect.github.com/pre-commit/pre-commit/issues/3404">#3404</a> from
  pre-commit/pre-commit-ci-update-config</li> <li><a
  href="https://github.com/pre-commit/pre-commit/commit/94b97e28f7cc7d9bcb536d7a3cf7ef6311e076fd"><code>94b97e2</code></a>
  [pre-commit.ci] pre-commit autoupdate</li> <li><a
  href="https://github.com/pre-commit/pre-commit/commit/2f93b804849e9237561417fbca29cb8d8ea4c905"><code>2f93b80</code></a>
  Merge pull request <a
  href="https://redirect.github.com/pre-commit/pre-commit/issues/3401">#3401</a> from
  pre-commit/pre-commit-ci-update-config</li> <li><a
  href="https://github.com/pre-commit/pre-commit/commit/4f90a1e88a80dd460f36e21d774d06bf0e73921b"><code>4f90a1e</code></a>
  [pre-commit.ci] pre-commit autoupdate</li> <li><a
  href="https://github.com/pre-commit/pre-commit/commit/aba1ce04e70162ca48b12f809ceffb253b788fe6"><code>aba1ce0</code></a>
  Merge pull request <a
  href="https://redirect.github.com/pre-commit/pre-commit/issues/3396">#3396</a> from
  pre-commit/all-repos_autofix_all-repos-sed</li> <li>Additional commits viewable in <a
  href="https://github.com/pre-commit/pre-commit/compare/v4.1.0...v4.2.0">compare view</a></li>
  </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=pre-commit&package-manager=pip&previous-version=4.1.0&new-version=4.2.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.8.0 to 2.8.1
  ([#561](https://github.com/Twingate/kubernetes-operator/pull/561),
  [`03be561`](https://github.com/Twingate/kubernetes-operator/commit/03be56195b9dbbb0316ed74883426c6a4a253e61))

Bumps [pydantic-settings](https://github.com/pydantic/pydantic-settings) from 2.8.0 to 2.8.1.
  <details> <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/pydantic/pydantic-settings/releases">pydantic-settings's
  releases</a>.</em></p> <blockquote> <h2>v2.8.1</h2> <h2>What's Changed</h2> <ul> <li>Fix for init
  source kwarg alias resolution. by <a href="https://github.com/kschwab"><code>@​kschwab</code></a>
  in <a
  href="https://redirect.github.com/pydantic/pydantic-settings/pull/550">pydantic/pydantic-settings#550</a></li>
  <li>Revert usage of positional only argument in <code>BaseSettings.__init__</code> by <a
  href="https://github.com/Viicos"><code>@​Viicos</code></a> in <a
  href="https://redirect.github.com/pydantic/pydantic-settings/pull/557">pydantic/pydantic-settings#557</a></li>
  <li>Revert use of <code>object</code> instead of <code>Any</code> by <a
  href="https://github.com/Viicos"><code>@​Viicos</code></a> in <a
  href="https://redirect.github.com/pydantic/pydantic-settings/pull/559">pydantic/pydantic-settings#559</a></li>
  <li>Prepare release 2.8.1 by <a href="https://github.com/hramezani"><code>@​hramezani</code></a>
  in <a
  href="https://redirect.github.com/pydantic/pydantic-settings/pull/558">pydantic/pydantic-settings#558</a></li>
  </ul> <p><strong>Full Changelog</strong>: <a
  href="https://github.com/pydantic/pydantic-settings/compare/v2.8.0...v2.8.1">https://github.com/pydantic/pydantic-settings/compare/v2.8.0...v2.8.1</a></p>
  </blockquote> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/pydantic/pydantic-settings/commit/5f33b6205608ccd51828cf52656b9b37f6c79db8"><code>5f33b62</code></a>
  Prepare release 2.8.1 (<a
  href="https://redirect.github.com/pydantic/pydantic-settings/issues/558">#558</a>)</li> <li><a
  href="https://github.com/pydantic/pydantic-settings/commit/fa64a4eebbf812cda0bfb83d95bd20b575a9ba14"><code>fa64a4e</code></a>
  Revert use of <code>object</code> instead of <code>Any</code> (<a
  href="https://redirect.github.com/pydantic/pydantic-settings/issues/559">#559</a>)</li> <li><a
  href="https://github.com/pydantic/pydantic-settings/commit/21e6b23cb768a258203a24034b5566fe2c8dd922"><code>21e6b23</code></a>
  Revert usage of positional only argument in <code>BaseSettings.__init__</code> (<a
  href="https://redirect.github.com/pydantic/pydantic-settings/issues/557">#557</a>)</li> <li><a
  href="https://github.com/pydantic/pydantic-settings/commit/1a4f3f43f96b1a8e973ede1e6e327af577a179e3"><code>1a4f3f4</code></a>
  Fix for init source kwarg alias resolution. (<a
  href="https://redirect.github.com/pydantic/pydantic-settings/issues/550">#550</a>)</li> <li>See
  full diff in <a
  href="https://github.com/pydantic/pydantic-settings/compare/v2.8.0...v2.8.1">compare view</a></li>
  </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=pydantic-settings&package-manager=pip&previous-version=2.8.0&new-version=2.8.1)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 8.3.4 to 8.3.5 ([#565](https://github.com/Twingate/kubernetes-operator/pull/565),
  [`a78e444`](https://github.com/Twingate/kubernetes-operator/commit/a78e444209aabf15b1123404a26754e3c21fe79e))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.3.4 to 8.3.5. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a
  href="https://github.com/pytest-dev/pytest/releases">pytest's releases</a>.</em></p> <blockquote>
  <h2>8.3.5</h2> <h1>pytest 8.3.5 (2025-03-02)</h1> <h2>Bug fixes</h2> <ul> <li><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/11777">#11777</a>: Fixed issue where
  sequences were still being shortened even with <code>-vv</code> verbosity.</li> <li><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/12888">#12888</a>: Fixed broken input
  when using Python 3.13+ and a <code>libedit</code> build of Python, such as on macOS or with
  uv-managed Python binaries from the <code>python-build-standalone</code> project. This could
  manifest e.g. by a broken prompt when using <code>Pdb</code>, or seeing empty inputs with manual
  usage of <code>input()</code> and suspended capturing.</li> <li><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13026">#13026</a>: Fixed
  <code>AttributeError</code>{.interpreted-text role=&quot;class&quot;} crash when using
  <code>--import-mode=importlib</code> when top-level directory same name as another module of the
  standard library.</li> <li><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13053">#13053</a>: Fixed a regression
  in pytest 8.3.4 where, when using <code>--import-mode=importlib</code>, a directory containing py
  file with the same name would cause an <code>ImportError</code></li> <li><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13083">#13083</a>: Fixed issue where
  pytest could crash if one of the collected directories got removed during collection.</li> </ul>
  <h2>Improved documentation</h2> <ul> <li> <p><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/12842">#12842</a>: Added dedicated page
  about using types with pytest.</p> <p>See <code>types</code>{.interpreted-text
  role=&quot;ref&quot;} for detailed usage.</p> </li> </ul> <h2>Contributor-facing changes</h2> <ul>
  <li><a href="https://redirect.github.com/pytest-dev/pytest/issues/13112">#13112</a>: Fixed
  selftest failures in <code>test_terminal.py</code> with Pygments &gt;= 2.19.0</li> <li><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13256">#13256</a>: Support for
  Towncrier versions released in 2024 has been re-enabled when building Sphinx docs -- by
  <code>webknjaz</code>{.interpreted-text role=&quot;user&quot;}.</li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/pytest-dev/pytest/commit/b55ab2aabb68c0ce94c3903139b062d0c2790152"><code>b55ab2a</code></a>
  Prepare release version 8.3.5</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/e217726d2a0edfaf58eae95bf835b85834b96da3"><code>e217726</code></a>
  Added dedicated page about using types with pytest <a
  href="https://redirect.github.com/pytest-dev/pytest/issues/12842">#12842</a> (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/12963">#12963</a>) (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13260">#13260</a>)</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/2fa3f8306c3da4aad7f7349a4947ac37ba6c652f"><code>2fa3f83</code></a>
  Add more resources and studies to flaky tests page in docs (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13250">#13250</a>) (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13259">#13259</a>)</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/e5c2efe3c36199731b41fd68bbf4df5e21404a8b"><code>e5c2efe</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/13256">#13256</a>
  from webknjaz/maintenance/towncrier-bump (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13258">#13258</a>)</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/3419674225a3a7b7d6f93650d75f6de52fe637d5"><code>3419674</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/13187">#13187</a>
  from pytest-dev/patchback/backports/8.3.x/b4009b319...</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/b75cfb162dbb927739698effa3fbcf279655da49"><code>b75cfb1</code></a>
  Add readline workaround for libedit (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13176">#13176</a>)</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/edbfff72a4051ed9c5f3d9b5d6f316b407cb6961"><code>edbfff7</code></a>
  doc: Clarify capturing .readouterr() return value (<a

href="https://redirect.github.com/pytest-dev/pytest/issues/13222">#13222</a>) (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13225">#13225</a>)</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/2ebba0063c66b77a7bd171221de059f3b3e47b86"><code>2ebba00</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/13199">#13199</a>
  from jakkdl/tox_docs_no_fetch (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13200">#13200</a>)</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/eb6496b79759f9acde581ed9d7a0777a49b5f820"><code>eb6496b</code></a>
  doc: Change training to remote only (<a

href="https://redirect.github.com/pytest-dev/pytest/issues/13196">#13196</a>) (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13197">#13197</a>)</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/78cf1f67f707fc07372a89775fd10d2065b5f17a"><code>78cf1f6</code></a>
  ci: Bump build-and-inspect-python-package (<a

href="https://redirect.github.com/pytest-dev/pytest/issues/13188">#13188</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/pytest-dev/pytest/compare/8.3.4...8.3.5">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=pytest&package-manager=pip&previous-version=8.3.4&new-version=8.3.5)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump responses from 0.25.6 to 0.25.7
  ([#573](https://github.com/Twingate/kubernetes-operator/pull/573),
  [`6c68c1e`](https://github.com/Twingate/kubernetes-operator/commit/6c68c1ed78799e03bb004c1ed83ba844595be52f))

Bumps [responses](https://github.com/getsentry/responses) from 0.25.6 to 0.25.7. <details>
  <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/getsentry/responses/releases">responses's releases</a>.</em></p>
  <blockquote> <h2>0.25.7</h2> <ul> <li>Added support for python 3.13</li> </ul> </blockquote>
  </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/getsentry/responses/blob/master/CHANGES">responses's
  changelog</a>.</em></p> <blockquote> <h2>0.25.7</h2> <ul> <li>Added support for python 3.13</li>
  </ul> </blockquote> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/getsentry/responses/commit/7fc249bd6f0849291474655ad78ca25816e6c6dd"><code>7fc249b</code></a>
  release: 0.25.7</li> <li><a
  href="https://github.com/getsentry/responses/commit/ba45c5d0a2e5c695061ad541191f874a69faef33"><code>ba45c5d</code></a>
  Update CHANGES (<a
  href="https://redirect.github.com/getsentry/responses/issues/760">#760</a>)</li> <li><a
  href="https://github.com/getsentry/responses/commit/d663d65073c4178a46265e24d66bd5d438073433"><code>d663d65</code></a>
  added pull request template (<a
  href="https://redirect.github.com/getsentry/responses/issues/759">#759</a>)</li> <li><a
  href="https://github.com/getsentry/responses/commit/a9e8beeb79500080ff0f01e9c811757d0b32285b"><code>a9e8bee</code></a>
  added support for Python 3.13 (<a
  href="https://redirect.github.com/getsentry/responses/issues/758">#758</a>)</li> <li><a
  href="https://github.com/getsentry/responses/commit/489b84768af3be97a2f6df6fabcc0dd8d749e2a9"><code>489b847</code></a>
  Merge branch 'release/0.25.6'</li> <li>See full diff in <a
  href="https://github.com/getsentry/responses/compare/0.25.6...0.25.7">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=responses&package-manager=pip&previous-version=0.25.6&new-version=0.25.7)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.10.0 to 0.11.0 ([#578](https://github.com/Twingate/kubernetes-operator/pull/578),
  [`5b618d3`](https://github.com/Twingate/kubernetes-operator/commit/5b618d3958d6caf33c79a4364e1f3faa5b0c9be2))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.10.0 to 0.11.0. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.11.0</h2> <h2>Release Notes</h2> <p>This is a follow-up
  to <a href="https://github.com/astral-sh/ruff/releases/tag/0.10.0">release 0.10.0</a>. The
  <code>requires-python</code> inference changes were unintentionally omitted from 0.10.0, and have
  been included here. This release also includes stabilization of the preview behavior for
  <code>PGH004</code>.</p> <h3>Breaking changes</h3> <ul> <li> <p><strong>Changes to how the Python
  version is inferred when a <code>target-version</code> is not specified</strong> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16319">#16319</a>)</p> <p>In previous
  versions of Ruff, you could specify your Python version with:</p> <ul> <li>The
  <code>target-version</code> option in a <code>ruff.toml</code> file or the
  <code>[tool.ruff]</code> section of a pyproject.toml file.</li> <li>The
  <code>project.requires-python</code> field in a <code>pyproject.toml</code> file with a
  <code>[tool.ruff]</code> section.</li> </ul> <p>These options worked well in most cases, and are
  still recommended for fine control of the Python version. However, because of the way Ruff
  discovers config files, <code>pyproject.toml</code> files without a <code>[tool.ruff]</code>
  section would be ignored, including the <code>requires-python</code> setting. Ruff would then use
  the default Python version (3.9 as of this writing) instead, which is surprising when you've
  attempted to request another version.</p> <p>In v0.10, config discovery has been updated to
  address this issue:</p> <ul> <li>If Ruff finds a <code>ruff.toml</code> file without a
  <code>target-version</code>, it will check for a <code>pyproject.toml</code> file in the same
  directory and respect its <code>requires-python</code> version, even if it does not contain a
  <code>[tool.ruff]</code> section.</li> <li>If Ruff finds a user-level configuration, the
  <code>requires-python</code> field of the closest <code>pyproject.toml</code> in a parent
  directory will take precedence.</li> <li>If there is no config file (<code>ruff.toml</code>or
  <code>pyproject.toml</code> with a <code>[tool.ruff]</code> section) in the directory of the file
  being checked, Ruff will search for the closest <code>pyproject.toml</code> in the parent
  directories and use its <code>requires-python</code> setting.</li> </ul> </li> </ul>
  <h3>Stabilization</h3> <p>The following behaviors have been stabilized:</p> <ul> <li><a
  href="https://docs.astral.sh/ruff/rules/blanket-noqa/"><code>blanket-noqa</code></a>
  (<code>PGH004</code>): Also detect blanked file-level noqa comments (and not just line level
  comments).</li> </ul> <h3>Preview features</h3> <ul> <li>[syntax-errors] Tuple unpacking in
  <code>for</code> statement iterator clause before Python 3.9 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16558">#16558</a>)</li> </ul> <h2>Install
  ruff 0.11.0</h2> <h3>Install prebuilt binaries via shell script</h3> <pre lang="sh"><code>curl
  --proto '=https' --tlsv1.2 -LsSf
  https://github.com/astral-sh/ruff/releases/download/0.11.0/ruff-installer.sh | sh </code></pre>
  <h3>Install prebuilt binaries via powershell script</h3> <pre lang="sh"><code>powershell
  -ExecutionPolicy ByPass -c &quot;irm
  https://github.com/astral-sh/ruff/releases/download/0.11.0/ruff-installer.ps1 | iex&quot;
  &lt;/tr&gt;&lt;/table&gt; </code></pre> </blockquote> <p>... (truncated)</p> </details> <details>
  <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
  <blockquote> <h2>0.11.0</h2> <p>This is a follow-up to release 0.10.0. Because of a mistake in the
  release process, the <code>requires-python</code> inference changes were not included in that
  release. Ruff 0.11.0 now includes this change as well as the stabilization of the preview behavior
  for <code>PGH004</code>.</p> <h3>Breaking changes</h3> <ul> <li> <p><strong>Changes to how the
  Python version is inferred when a <code>target-version</code> is not specified</strong> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16319">#16319</a>)</p> <p>In previous
  versions of Ruff, you could specify your Python version with:</p> <ul> <li>The
  <code>target-version</code> option in a <code>ruff.toml</code> file or the
  <code>[tool.ruff]</code> section of a pyproject.toml file.</li> <li>The
  <code>project.requires-python</code> field in a <code>pyproject.toml</code> file with a
  <code>[tool.ruff]</code> section.</li> </ul> <p>These options worked well in most cases, and are
  still recommended for fine control of the Python version. However, because of the way Ruff
  discovers config files, <code>pyproject.toml</code> files without a <code>[tool.ruff]</code>
  section would be ignored, including the <code>requires-python</code> setting. Ruff would then use
  the default Python version (3.9 as of this writing) instead, which is surprising when you've
  attempted to request another version.</p> <p>In v0.10, config discovery has been updated to
  address this issue:</p> <ul> <li>If Ruff finds a <code>ruff.toml</code> file without a
  <code>target-version</code>, it will check for a <code>pyproject.toml</code> file in the same
  directory and respect its <code>requires-python</code> version, even if it does not contain a
  <code>[tool.ruff]</code> section.</li> <li>If Ruff finds a user-level configuration, the
  <code>requires-python</code> field of the closest <code>pyproject.toml</code> in a parent
  directory will take precedence.</li> <li>If there is no config file (<code>ruff.toml</code>or
  <code>pyproject.toml</code> with a <code>[tool.ruff]</code> section) in the directory of the file
  being checked, Ruff will search for the closest <code>pyproject.toml</code> in the parent
  directories and use its <code>requires-python</code> setting.</li> </ul> </li> </ul>
  <h3>Stabilization</h3> <p>The following behaviors have been stabilized:</p> <ul> <li><a
  href="https://docs.astral.sh/ruff/rules/blanket-noqa/"><code>blanket-noqa</code></a>
  (<code>PGH004</code>): Also detect blanked file-level noqa comments (and not just line level
  comments).</li> </ul> <h3>Preview features</h3> <ul> <li>[syntax-errors] Tuple unpacking in
  <code>for</code> statement iterator clause before Python 3.9 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16558">#16558</a>)</li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ruff/commit/2cd25ef6410fb5fca96af1578728a3d828d2d53a"><code>2cd25ef</code></a>
  Ruff 0.11.0 (<a href="https://redirect.github.com/astral-sh/ruff/issues/16723">#16723</a>)</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/a22d206db265a2c8a1f8306cef61c5c1808ebf52"><code>a22d206</code></a>
  [red-knot] Preliminary tests for typing.Final (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/15917">#15917</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/270318c2e023aaf4f04aa56ea2bf6f8d426b16b7"><code>270318c</code></a>
  [red-knot] fix: improve type inference for binary ops on tuples (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16725">#16725</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/d03b12e711ce2ef85bb3308bd698b8be4b636761"><code>d03b12e</code></a>
  [red-knot] Assignments to attributes (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16705">#16705</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/14c5ed5d7dc8c51e3436e06e5e4d15bb7f7aa9c5"><code>14c5ed5</code></a>
  [<code>pygrep-hooks</code>]: Detect file-level suppressions comments without rul… (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16720">#16720</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/595565015bfc932ca7bb28047a7204d1b84bd8ab"><code>5955650</code></a>
  Fallback to requires-python in certain cases when target-version is not found...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/2382fe1f256049615a8914a3778660acc45fc74c"><code>2382fe1</code></a>
  [syntax-errors] Tuple unpacking in <code>for</code> statement iterator clause before Pyt...</li>
  <li>See full diff in <a href="https://github.com/astral-sh/ruff/compare/0.10.0...0.11.0">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ruff&package-manager=pip&previous-version=0.10.0&new-version=0.11.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.11.0 to 0.11.2 ([#582](https://github.com/Twingate/kubernetes-operator/pull/582),
  [`3de31fe`](https://github.com/Twingate/kubernetes-operator/commit/3de31fee04bbcc579c37fccfd87f93e8f7ae9593))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.11.0 to 0.11.2. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.11.2</h2> <h2>Release Notes</h2> <h3>Preview
  features</h3> <ul> <li>[syntax-errors] Fix false-positive syntax errors emitted for annotations on
  variadic parameters before Python 3.11 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16878">#16878</a>)</li> </ul>
  <h2>Contributors</h2> <ul> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> <li><a
  href="https://github.com/MatthewMckee4"><code>@​MatthewMckee4</code></a></li> <li><a
  href="https://github.com/dhruvmanila"><code>@​dhruvmanila</code></a></li> <li><a
  href="https://github.com/junhsonjb"><code>@​junhsonjb</code></a></li> <li><a
  href="https://github.com/mtshiba"><code>@​mtshiba</code></a></li> <li><a
  href="https://github.com/ntBre"><code>@​ntBre</code></a></li> </ul> <h2>Install ruff 0.11.2</h2>
  <h3>Install prebuilt binaries via shell script</h3> <pre lang="sh"><code>curl --proto '=https'
  --tlsv1.2 -LsSf https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-installer.sh | sh
  </code></pre> <h3>Install prebuilt binaries via powershell script</h3> <pre
  lang="sh"><code>powershell -ExecutionPolicy ByPass -c &quot;irm
  https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-installer.ps1 | iex&quot;
  </code></pre> <h2>Download ruff 0.11.2</h2> <table> <thead> <tr> <th>File</th> <th>Platform</th>
  <th>Checksum</th> </tr> </thead> <tbody> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-aarch64-apple-darwin.tar.gz">ruff-aarch64-apple-darwin.tar.gz</a></td>
  <td>Apple Silicon macOS</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-aarch64-apple-darwin.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-x86_64-apple-darwin.tar.gz">ruff-x86_64-apple-darwin.tar.gz</a></td>
  <td>Intel macOS</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-x86_64-apple-darwin.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-aarch64-pc-windows-msvc.zip">ruff-aarch64-pc-windows-msvc.zip</a></td>
  <td>ARM64 Windows</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-aarch64-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-i686-pc-windows-msvc.zip">ruff-i686-pc-windows-msvc.zip</a></td>
  <td>x86 Windows</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-i686-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-x86_64-pc-windows-msvc.zip">ruff-x86_64-pc-windows-msvc.zip</a></td>
  <td>x64 Windows</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-x86_64-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-aarch64-unknown-linux-gnu.tar.gz">ruff-aarch64-unknown-linux-gnu.tar.gz</a></td>
  <td>ARM64 Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-aarch64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-i686-unknown-linux-gnu.tar.gz">ruff-i686-unknown-linux-gnu.tar.gz</a></td>
  <td>x86 Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-i686-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-powerpc64-unknown-linux-gnu.tar.gz">ruff-powerpc64-unknown-linux-gnu.tar.gz</a></td>
  <td>PPC64 Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-powerpc64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-powerpc64le-unknown-linux-gnu.tar.gz">ruff-powerpc64le-unknown-linux-gnu.tar.gz</a></td>
  <td>PPC64LE Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-powerpc64le-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-s390x-unknown-linux-gnu.tar.gz">ruff-s390x-unknown-linux-gnu.tar.gz</a></td>
  <td>S390x Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-s390x-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-x86_64-unknown-linux-gnu.tar.gz">ruff-x86_64-unknown-linux-gnu.tar.gz</a></td>
  <td>x64 Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-x86_64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-armv7-unknown-linux-gnueabihf.tar.gz">ruff-armv7-unknown-linux-gnueabihf.tar.gz</a></td>
  <td>ARMv7 Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-armv7-unknown-linux-gnueabihf.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-aarch64-unknown-linux-musl.tar.gz">ruff-aarch64-unknown-linux-musl.tar.gz</a></td>
  <td>ARM64 MUSL Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-aarch64-unknown-linux-musl.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-i686-unknown-linux-musl.tar.gz">ruff-i686-unknown-linux-musl.tar.gz</a></td>
  <td>x86 MUSL Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-i686-unknown-linux-musl.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-x86_64-unknown-linux-musl.tar.gz">ruff-x86_64-unknown-linux-musl.tar.gz</a></td>
  <td>x64 MUSL Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-x86_64-unknown-linux-musl.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-arm-unknown-linux-musleabihf.tar.gz">ruff-arm-unknown-linux-musleabihf.tar.gz</a></td>
  <td>ARMv6 MUSL Linux (Hardfloat)</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.11.2/ruff-arm-unknown-linux-musleabihf.tar.gz.sha256">checksum</a></td>
  </tr> </tbody> </table> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details>
  <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
  <blockquote> <h2>0.11.2</h2> <h3>Preview features</h3> <ul> <li>[syntax-errors] Fix false-positive
  syntax errors emitted for annotations on variadic parameters before Python 3.11 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16878">#16878</a>)</li> </ul>
  <h2>0.11.1</h2> <h3>Preview features</h3> <ul> <li>[<code>airflow</code>] Add <code>chain</code>,
  <code>chain_linear</code> and <code>cross_downstream</code> for <code>AIR302</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16647">#16647</a>)</li> <li>[syntax-errors]
  Improve error message and range for pre-PEP-614 decorator syntax errors (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16581">#16581</a>)</li> <li>[syntax-errors]
  PEP 701 f-strings before Python 3.12 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16543">#16543</a>)</li> <li>[syntax-errors]
  Parenthesized context managers before Python 3.9 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16523">#16523</a>)</li> <li>[syntax-errors]
  Star annotations before Python 3.11 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16545">#16545</a>)</li> <li>[syntax-errors]
  Star expression in index before Python 3.11 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16544">#16544</a>)</li> <li>[syntax-errors]
  Unparenthesized assignment expressions in sets and indexes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16404">#16404</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>Server: Allow <code>FixAll</code> action in presence of version-specific
  syntax errors (<a href="https://redirect.github.com/astral-sh/ruff/pull/16848">#16848</a>)</li>
  <li>[<code>flake8-bandit</code>] Allow raw strings in <code>suspicious-mark-safe-usage</code>
  (<code>S308</code>) <a href="https://redirect.github.com/astral-sh/ruff/issues/16702">#16702</a>
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/16770">#16770</a>)</li>
  <li>[<code>refurb</code>] Avoid panicking <code>unwrap</code> in
  <code>verbose-decimal-constructor</code> (<code>FURB157</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16777">#16777</a>)</li>
  <li>[<code>refurb</code>] Fix starred expressions fix (<code>FURB161</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16550">#16550</a>)</li> <li>Fix
  <code>--statistics</code> reporting for unsafe fixes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16756">#16756</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>flake8-executables</code>] Allow <code>uv run</code> in shebang line
  for <code>shebang-missing-python</code> (<code>EXE003</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16849">#16849</a>,<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16855">#16855</a>)</li> </ul> <h3>CLI</h3>
  <ul> <li>Add <code>--exit-non-zero-on-format</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16009">#16009</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Update Ruff tutorial to avoid non-existent fix in
  <code>__init__.py</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16818">#16818</a>)</li>
  <li>[<code>flake8-gettext</code>] Swap <code>format-</code> and
  <code>printf-in-get-text-func-call</code> examples (<code>INT002</code>, <code>INT003</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16769">#16769</a>)</li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ruff/commit/4773878ee70ea9b700d3d57c3ca4a917c7d8ea38"><code>4773878</code></a>
  Bump 0.11.2 (<a href="https://redirect.github.com/astral-sh/ruff/issues/16896">#16896</a>)</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/2a4d8351325d97e3a2dd4a0fcc489cce15561dc1"><code>2a4d835</code></a>
  Use the common <code>OperatorPrecedence</code> for the parser (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16747">#16747</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/04a875637954c8f88eb39a2fdf815be899bec1bb"><code>04a8756</code></a>
  [red-knot] Check subtype relation between callable types (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16804">#16804</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/193c38199e10b57f7b3ebeefca390ce50401e697"><code>193c381</code></a>
  [red-knot] Check whether two callable types are equivalent (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16698">#16698</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/63e78b41cdcb6e5469998fe4fba97260b3a3e95c"><code>63e78b4</code></a>
  [red-knot] Ban most <code>Type::Instance</code> types in type expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16872">#16872</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/296d67a496f4261fe5e0734b81e0f8b91a1de312"><code>296d67a</code></a>
  Special-case value-expression inference of special form subscriptions (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16877">#16877</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/42cbce538b57961231b20fca524bbc16e857f5c3"><code>42cbce5</code></a>
  [syntax-errors] Fix star annotation before Python 3.11 (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16878">#16878</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/67602512b6cc90dad377b8b8709b981a6184fe37"><code>6760251</code></a>
  Recognize <code>SyntaxError:</code> as an error code for ecosystem checks (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16879">#16879</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/23382f5f8c7b4e356368cdeb1049b8c1910baff3"><code>23382f5</code></a>
  [red-knot] add test cases result in false positive errors (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16856">#16856</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/c1971fdde24b37e64baa70386d933715aeec13c6"><code>c1971fd</code></a>
  Bump 0.11.1 (<a href="https://redirect.github.com/astral-sh/ruff/issues/16871">#16871</a>)</li>
  <li>Additional commits viewable in <a
  href="https://github.com/astral-sh/ruff/compare/0.11.0...0.11.2">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ruff&package-manager=pip&previous-version=0.11.0&new-version=0.11.2)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.9.10 to 0.10.0 ([#576](https://github.com/Twingate/kubernetes-operator/pull/576),
  [`6cc42e7`](https://github.com/Twingate/kubernetes-operator/commit/6cc42e7d54c1df34e087fdf774d00858f2c22dbe))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.9.10 to 0.10.0. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.10.0</h2> <h2>Release Notes</h2> <p>Check out the <a
  href="https://astral.sh/blog/ruff-v0.10.0">blog post</a> for a migration guide and overview of the
  changes!</p> <h3>Breaking changes</h3> <p>See also, the &quot;Remapped rules&quot; section which
  may result in disabled rules.</p> <ul> <li> <p><strong>Changes to how the Python version is
  inferred when a <code>target-version</code> is not specified</strong> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16319">#16319</a>)</p> <p>In previous
  versions of Ruff, you could specify your Python version with:</p> <ul> <li>The
  <code>target-version</code> option in a <code>ruff.toml</code> file or the
  <code>[tool.ruff]</code> section of a pyproject.toml file.</li> <li>The
  <code>project.requires-python</code> field in a <code>pyproject.toml</code> file with a
  <code>[tool.ruff]</code> section.</li> </ul> <p>These options worked well in most cases, and are
  still recommended for fine control of the Python version. However, because of the way Ruff
  discovers config files, <code>pyproject.toml</code> files without a <code>[tool.ruff]</code>
  section would be ignored, including the <code>requires-python</code> setting. Ruff would then use
  the default Python version (3.9 as of this writing) instead, which is surprising when you've
  attempted to request another version.</p> <p>In v0.10, config discovery has been updated to
  address this issue:</p> <ul> <li>If Ruff finds a <code>ruff.toml</code> file without a
  <code>target-version</code>, it will check for a <code>pyproject.toml</code> file in the same
  directory and respect its <code>requires-python</code> version, even if it does not contain a
  <code>[tool.ruff]</code> section.</li> <li>If Ruff finds a user-level configuration, the
  <code>requires-python</code> field of the closest <code>pyproject.toml</code> in a parent
  directory will take precedence.</li> <li>If there is no config file (<code>ruff.toml</code>or
  <code>pyproject.toml</code> with a <code>[tool.ruff]</code> section) in the directory of the file
  being checked, Ruff will search for the closest <code>pyproject.toml</code> in the parent
  directories and use its <code>requires-python</code> setting.</li> </ul> </li> <li>
  <p><strong>Updated <code>TYPE_CHECKING</code> behavior</strong> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16669">#16669</a>)</p> <p>Previously, Ruff
  only recognized typechecking blocks that tested the <code>typing.TYPE_CHECKING</code> symbol. Now,
  Ruff recognizes any local variable named <code>TYPE_CHECKING</code>. This release also removes
  support for the legacy <code>if 0:</code> and <code>if False:</code> typechecking checks. Use a
  local <code>TYPE_CHECKING</code> variable instead.</p> </li> <li> <p><strong>More robust noqa
  parsing</strong> (<a href="https://redirect.github.com/astral-sh/ruff/pull/16483">#16483</a>)</p>
  <p>The syntax for both file-level and in-line suppression comments has been unified and made more
  robust to certain errors. In most cases, this will result in more suppression comments being read
  by Ruff, but there are a few instances where previously read comments will now log an error to the
  user instead. Please refer to the documentation on <a
  href="https://docs.astral.sh/ruff/linter/#error-suppression"><em>Error suppression</em></a> for
  the full specification.</p> </li> <li> <p><strong>Avoid unnecessary parentheses around with
  statements with a single context manager and a trailing comment</strong> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/14005">#14005</a>)</p> <p>This change fixes
  a bug in the formatter where it introduced unnecessary parentheses around with statements with a
  single context manager and a trailing comment. This change may result in a change in formatting
  for some users.</p> </li> <li> <p><strong>Bump alpine default tag to 3.21 for derived Docker
  images</strong> (<a href="https://redirect.github.com/astral-sh/ruff/pull/16456">#16456</a>)</p>
  <p>Alpine 3.21 was released in Dec 2024 and is used in the official Alpine-based Python images.
  Now the ruff:alpine image will use 3.21 instead of 3.20 and ruff:alpine3.20 will no longer be
  updated.</p> </li> </ul> <h3>Deprecated Rules</h3> <p>The following rules have been
  deprecated:</p> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details>
  <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
  <blockquote> <h2>0.10.0</h2> <p>Check out the <a href="https://astral.sh/blog/ruff-v0.10.0">blog
  post</a> for a migration guide and overview of the changes!</p> <h3>Breaking changes</h3> <p>See
  also, the &quot;Remapped rules&quot; section which may result in disabled rules.</p> <ul> <li>
  <p><strong>Changes to how the Python version is inferred when a <code>target-version</code> is not
  specified</strong> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16319">#16319</a>)</p> <p>Because of a
  mistake in the release process, the <code>requires-python</code> inference changes are not
  included in this release and instead shipped as part of 0.11.0. You can find a description of this
  change in the 0.11.0 section.</p> </li> <li> <p><strong>Updated <code>TYPE_CHECKING</code>
  behavior</strong> (<a href="https://redirect.github.com/astral-sh/ruff/pull/16669">#16669</a>)</p>
  <p>Previously, Ruff only recognized typechecking blocks that tested the
  <code>typing.TYPE_CHECKING</code> symbol. Now, Ruff recognizes any local variable named
  <code>TYPE_CHECKING</code>. This release also removes support for the legacy <code>if 0:</code>
  and <code>if False:</code> typechecking checks. Use a local <code>TYPE_CHECKING</code> variable
  instead.</p> </li> <li> <p><strong>More robust noqa parsing</strong> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16483">#16483</a>)</p> <p>The syntax for
  both file-level and in-line suppression comments has been unified and made more robust to certain
  errors. In most cases, this will result in more suppression comments being read by Ruff, but there
  are a few instances where previously read comments will now log an error to the user instead.
  Please refer to the documentation on <a
  href="https://docs.astral.sh/ruff/linter/#error-suppression"><em>Error suppression</em></a> for
  the full specification.</p> </li> <li> <p><strong>Avoid unnecessary parentheses around with
  statements with a single context manager and a trailing comment</strong> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/14005">#14005</a>)</p> <p>This change fixes
  a bug in the formatter where it introduced unnecessary parentheses around with statements with a
  single context manager and a trailing comment. This change may result in a change in formatting
  for some users.</p> </li> <li> <p><strong>Bump alpine default tag to 3.21 for derived Docker
  images</strong> (<a href="https://redirect.github.com/astral-sh/ruff/pull/16456">#16456</a>)</p>
  <p>Alpine 3.21 was released in Dec 2024 and is used in the official Alpine-based Python images.
  Now the ruff:alpine image will use 3.21 instead of 3.20 and ruff:alpine3.20 will no longer be
  updated.</p> </li> </ul> <h3>Deprecated Rules</h3> <p>The following rules have been
  deprecated:</p> <ul> <li><a
  href="https://docs.astral.sh/ruff/rules/non-pep604-isinstance/"><code>non-pep604-isinstance</code></a>
  (<code>UP038</code>)</li> <li><a
  href="https://docs.astral.sh/ruff/rules/suspicious-xmle-tree-usage/"><code>suspicious-xmle-tree-usage</code></a>
  (<code>S320</code>)</li> </ul> <h3>Remapped rules</h3> <p>The following rules have been remapped
  to new rule codes:</p> <ul> <li>[<code>unsafe-markup-use</code>]: <code>RUF035</code> to
  <code>S704</code></li> </ul> <h3>Stabilization</h3> <p>The following rules have been stabilized
  and are no longer in preview:</p> <ul> <li><a
  href="https://docs.astral.sh/ruff/rules/batched-without-explicit-strict"><code>batched-without-explicit-strict</code></a>
  (<code>B911</code>)</li> <li><a
  href="https://docs.astral.sh/ruff/rules/unnecessary-dict-comprehension-for-iterable"><code>unnecessary-dict-comprehension-for-iterable</code></a>
  (<code>C420</code>)</li> <li><a
  href="https://docs.astral.sh/ruff/rules/datetime-min-max"><code>datetime-min-max</code></a>
  (<code>DTZ901</code>)</li> <li><a
  href="https://docs.astral.sh/ruff/rules/fast-api-unused-path-parameter"><code>fast-api-unused-path-parameter</code></a>
  (<code>FAST003</code>)</li> </ul> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ruff/commit/27e9d1fe3e60a0b6731ba3be103a48a33b8e3a7c"><code>27e9d1f</code></a>
  Ruff v0.10 Release (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16708">#16708</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/acf35c55f8b8f5ce16ac388e7f6a1af884edbe16"><code>acf35c5</code></a>
  Add new <code>noqa</code> specification to the docs (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16703">#16703</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/b9b256209bee472c65a45ecd3b7e5cc34653a9bf"><code>b9b2562</code></a>
  describe requires-python fallback in docs (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16704">#16704</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/abaa18993b285a183ba326cf92ab4e5ba0199cea"><code>abaa189</code></a>
  [red-knot] handle cycles in MRO/bases resolution (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16693">#16693</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/360ba095ffc7dbbdb175fbaab011c25bcb4ae48a"><code>360ba09</code></a>
  [red-knot] Auto generate statement nodes (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16645">#16645</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/d8159e816f161df90b35a8c569d93b9381568b9f"><code>d8159e8</code></a>
  [<code>pylint</code>] Better inference for <code>str.strip</code> (<code>PLE310</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16671">#16671</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/04ad562afd8a08ba0863780f855ebf39446effff"><code>04ad562</code></a>
  [<code>pylint</code>] Improve <code>repeated-equality-comparison</code> fix to use a
  <code>set</code> when all...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/91674718c41e4e11beeaa38c78a368760137e2b8"><code>9167471</code></a>
  [<code>pylint</code>/<code>pep8-naming</code>] Check <code>__new__</code> argument name in
  `bad-staticmethod-a...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/348815d6d6c1e126ac2175463233de4c56c763eb"><code>348815d</code></a>
  [<code>flake8-pyi</code>] Stabilize fix for <code>unused-private-type-var</code>
  (<code>PYI018</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16682">#16682</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/1326d55c291fb563cc6c16b11c358d5e9f12e8bd"><code>1326d55</code></a>
  [<code>flake8-bandit</code>] Deprecate <code>suspicious-xmle-tree-usage</code> (<code>S320</code>)
  (<a href="https://redirect.github.com/astral-sh/ruff/issues/16680">#16680</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.9.10...0.10.0">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ruff&package-manager=pip&previous-version=0.9.10&new-version=0.10.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

---------

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <205185+ekampf@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

- Bump ruff from 0.9.7 to 0.9.9 ([#566](https://github.com/Twingate/kubernetes-operator/pull/566),
  [`bcd9020`](https://github.com/Twingate/kubernetes-operator/commit/bcd9020308f09fda5d2e3a90c10bc7647d53b1dd))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.9.7 to 0.9.9. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.9.9</h2> <h2>Release Notes</h2> <h3>Preview
  features</h3> <ul> <li>Fix caching of unsupported-syntax errors (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16425">#16425</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>Only show unsupported-syntax errors in editors when preview mode is enabled
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/16429">#16429</a>)</li> </ul>
  <h2>Contributors</h2> <ul> <li><a
  href="https://github.com/InSyncWithFoo"><code>@​InSyncWithFoo</code></a></li> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/dhruvmanila"><code>@​dhruvmanila</code></a></li> <li><a
  href="https://github.com/ntBre"><code>@​ntBre</code></a></li> </ul> <h2>Install ruff 0.9.9</h2>
  <h3>Install prebuilt binaries via shell script</h3> <pre lang="sh"><code>curl --proto '=https'
  --tlsv1.2 -LsSf https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-installer.sh | sh
  </code></pre> <h3>Install prebuilt binaries via powershell script</h3> <pre
  lang="sh"><code>powershell -ExecutionPolicy ByPass -c &quot;irm
  https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-installer.ps1 | iex&quot;
  </code></pre> <h2>Download ruff 0.9.9</h2> <table> <thead> <tr> <th>File</th> <th>Platform</th>
  <th>Checksum</th> </tr> </thead> <tbody> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-aarch64-apple-darwin.tar.gz">ruff-aarch64-apple-darwin.tar.gz</a></td>
  <td>Apple Silicon macOS</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-aarch64-apple-darwin.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-x86_64-apple-darwin.tar.gz">ruff-x86_64-apple-darwin.tar.gz</a></td>
  <td>Intel macOS</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-x86_64-apple-darwin.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-aarch64-pc-windows-msvc.zip">ruff-aarch64-pc-windows-msvc.zip</a></td>
  <td>ARM64 Windows</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-aarch64-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-i686-pc-windows-msvc.zip">ruff-i686-pc-windows-msvc.zip</a></td>
  <td>x86 Windows</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-i686-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-x86_64-pc-windows-msvc.zip">ruff-x86_64-pc-windows-msvc.zip</a></td>
  <td>x64 Windows</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-x86_64-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-aarch64-unknown-linux-gnu.tar.gz">ruff-aarch64-unknown-linux-gnu.tar.gz</a></td>
  <td>ARM64 Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-aarch64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-i686-unknown-linux-gnu.tar.gz">ruff-i686-unknown-linux-gnu.tar.gz</a></td>
  <td>x86 Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-i686-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-powerpc64-unknown-linux-gnu.tar.gz">ruff-powerpc64-unknown-linux-gnu.tar.gz</a></td>
  <td>PPC64 Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-powerpc64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-powerpc64le-unknown-linux-gnu.tar.gz">ruff-powerpc64le-unknown-linux-gnu.tar.gz</a></td>
  <td>PPC64LE Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-powerpc64le-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-s390x-unknown-linux-gnu.tar.gz">ruff-s390x-unknown-linux-gnu.tar.gz</a></td>
  <td>S390x Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-s390x-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-x86_64-unknown-linux-gnu.tar.gz">ruff-x86_64-unknown-linux-gnu.tar.gz</a></td>
  <td>x64 Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-x86_64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-armv7-unknown-linux-gnueabihf.tar.gz">ruff-armv7-unknown-linux-gnueabihf.tar.gz</a></td>
  <td>ARMv7 Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-armv7-unknown-linux-gnueabihf.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-aarch64-unknown-linux-musl.tar.gz">ruff-aarch64-unknown-linux-musl.tar.gz</a></td>
  <td>ARM64 MUSL Linux</td> <td><a
  href="https://github.com/astral-sh/ruff/releases/download/0.9.9/ruff-aarch64-unknown-linux-musl.tar.gz.sha256">checksum</a></td>
  </tr> </tbody> </table> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details>
  <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
  <blockquote> <h2>0.9.9</h2> <h3>Preview features</h3> <ul> <li>Fix caching of unsupported-syntax
  errors (<a href="https://redirect.github.com/astral-sh/ruff/pull/16425">#16425</a>)</li> </ul>
  <h3>Bug fixes</h3> <ul> <li>Only show unsupported-syntax errors in editors when preview mode is
  enabled (<a href="https://redirect.github.com/astral-sh/ruff/pull/16429">#16429</a>)</li> </ul>
  <h2>0.9.8</h2> <h3>Preview features</h3> <ul> <li>Start detecting version-related syntax errors in
  the parser (<a href="https://redirect.github.com/astral-sh/ruff/pull/16090">#16090</a>)</li> </ul>
  <h3>Rule changes</h3> <ul> <li>[<code>pylint</code>] Mark fix unsafe (<code>PLW1507</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16343">#16343</a>)</li>
  <li>[<code>pylint</code>] Catch <code>case np.nan</code>/<code>case math.nan</code> in
  <code>match</code> statements (<code>PLW0177</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16378">#16378</a>)</li>
  <li>[<code>ruff</code>] Add more Pydantic models variants to the list of default copy semantics
  (<code>RUF012</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16291">#16291</a>)</li> </ul>
  <h3>Server</h3> <ul> <li>Avoid indexing the project if <code>configurationPreference</code> is
  <code>editorOnly</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16381">#16381</a>)</li> <li>Avoid
  unnecessary info at non-trace server log level (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16389">#16389</a>)</li> <li>Expand
  <code>ruff.configuration</code> to allow inline config (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16296">#16296</a>)</li> <li>Notify users for
  invalid client settings (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16361">#16361</a>)</li> </ul>
  <h3>Configuration</h3> <ul> <li>Add <code>per-file-target-version</code> option (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16257">#16257</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>[<code>refurb</code>] Do not consider docstring(s) (<code>FURB156</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16391">#16391</a>)</li>
  <li>[<code>flake8-self</code>] Ignore attribute accesses on instance-like variables
  (<code>SLF001</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16149">#16149</a>)</li>
  <li>[<code>pylint</code>] Fix false positives, add missing methods, and support positional-only
  parameters (<code>PLE0302</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16263">#16263</a>)</li>
  <li>[<code>flake8-pyi</code>] Mark <code>PYI030</code> fix unsafe when comments are deleted (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16322">#16322</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Fix example for <code>S611</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16316">#16316</a>)</li> <li>Normalize
  inconsistent markdown headings in docstrings (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16364">#16364</a>)</li> <li>Document MSRV
  policy (<a href="https://redirect.github.com/astral-sh/ruff/pull/16384">#16384</a>)</li> </ul>
  </blockquote> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ruff/commit/091d0af2ab026a08b82d4aa7d3ab6b1ca4db778c"><code>091d0af</code></a>
  Bump version to Ruff 0.9.9 (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16434">#16434</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/3d72138740ed8c3ec9f733ace10fd40af0ff77eb"><code>3d72138</code></a>
  Check <code>LinterSettings::preview</code> for version-related syntax errors (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16429">#16429</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/4a237560244ecc1c2b4217724bcbaf605c844468"><code>4a23756</code></a>
  Avoid caching files with unsupported syntax errors (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16425">#16425</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/af62f7932bfee8a35b411c8351fbb81068caf7a6"><code>af62f79</code></a>
  Prioritize &quot;bug&quot; label for changelog sections (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16433">#16433</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/0ced8d053c2ff6ff86f3329f24c7c0854fa8466b"><code>0ced8d0</code></a>
  [<code>flake8-copyright</code>] Add links to applicable options (<code>CPY001</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16421">#16421</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/a8e171f82c14d7a6d617b204eca39978eb2ad2df"><code>a8e171f</code></a>
  Fix string-length limit in documentation for PYI054 (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16432">#16432</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/cf83584abb130574059064ad5f0dd806c22e45d5"><code>cf83584</code></a>
  Show version-related syntax errors in the playground (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16419">#16419</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/764aa0e6a1b16284c1c939332c19d742dae8aee1"><code>764aa0e</code></a>
  Allow passing <code>ParseOptions</code> to inline tests (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16357">#16357</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/568cf88c6c5b5551a675ae2b13deedec0fe226cb"><code>568cf88</code></a>
  Bump version to 0.9.8 (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16414">#16414</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/040071bbc5b21306f2759693ca6ee2c3fc5420bf"><code>040071b</code></a>
  [red-knot] Ignore surrounding whitespace when looking for `&lt;!-- snapshot-diag...</li>
  <li>Additional commits viewable in <a
  href="https://github.com/astral-sh/ruff/compare/0.9.7...0.9.9">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ruff&package-manager=pip&previous-version=0.9.7&new-version=0.9.9)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.9.9 to 0.9.10 ([#571](https://github.com/Twingate/kubernetes-operator/pull/571),
  [`b030bf6`](https://github.com/Twingate/kubernetes-operator/commit/b030bf6dec1d3ea6c1cc6740b5c75c4e339ae9e3))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.9.9 to 0.9.10. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.9.10</h2> <h2>Release Notes</h2> <h3>Preview
  features</h3> <ul> <li>[<code>ruff</code>] Add new rule <code>RUF059</code>: Unused unpacked
  assignment (<a href="https://redirect.github.com/astral-sh/ruff/pull/16449">#16449</a>)</li>
  <li>[<code>syntax-errors</code>] Detect assignment expressions before Python 3.8 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16383">#16383</a>)</li>
  <li>[<code>syntax-errors</code>] Named expressions in decorators before Python 3.9 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16386">#16386</a>)</li>
  <li>[<code>syntax-errors</code>] Parenthesized keyword argument names after Python 3.8 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16482">#16482</a>)</li>
  <li>[<code>syntax-errors</code>] Positional-only parameters before Python 3.8 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16481">#16481</a>)</li>
  <li>[<code>syntax-errors</code>] Tuple unpacking in <code>return</code> and <code>yield</code>
  before Python 3.8 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16485">#16485</a>)</li>
  <li>[<code>syntax-errors</code>] Type parameter defaults before Python 3.13 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16447">#16447</a>)</li>
  <li>[<code>syntax-errors</code>] Type parameter lists before Python 3.12 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16479">#16479</a>)</li>
  <li>[<code>syntax-errors</code>] <code>except*</code> before Python 3.11 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16446">#16446</a>)</li>
  <li>[<code>syntax-errors</code>] <code>type</code> statements before Python 3.12 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16478">#16478</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>Escape template filenames in glob patterns in configuration (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16407">#16407</a>)</li>
  <li>[<code>flake8-simplify</code>] Exempt unittest context methods for <code>SIM115</code> rule
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/16439">#16439</a>)</li> <li>Formatter:
  Fix syntax error location in notebooks (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16499">#16499</a>)</li>
  <li>[<code>pyupgrade</code>] Do not offer fix when at least one target is
  <code>global</code>/<code>nonlocal</code> (<code>UP028</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16451">#16451</a>)</li>
  <li>[<code>flake8-builtins</code>] Ignore variables matching module attribute names
  (<code>A001</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16454">#16454</a>)</li>
  <li>[<code>pylint</code>] Convert <code>code</code> keyword argument to a positional argument in
  fix for (<code>PLR1722</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16424">#16424</a>)</li> </ul> <h3>CLI</h3>
  <ul> <li>Move rule code from <code>description</code> to <code>check_name</code> in GitLab output
  serializer (<a href="https://redirect.github.com/astral-sh/ruff/pull/16437">#16437</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>[<code>pydocstyle</code>] Clarify that <code>D417</code> only
  checks docstrings with an arguments section (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16494">#16494</a>)</li> </ul>
  <h2>Contributors</h2> <ul> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> <li><a
  href="https://github.com/BurntSushi"><code>@​BurntSushi</code></a></li> <li><a
  href="https://github.com/Glyphack"><code>@​Glyphack</code></a></li> <li><a
  href="https://github.com/InSyncWithFoo"><code>@​InSyncWithFoo</code></a></li> <li><a
  href="https://github.com/JelleZijlstra"><code>@​JelleZijlstra</code></a></li> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/VascoSch92"><code>@​VascoSch92</code></a></li> <li><a
  href="https://github.com/adamchainz"><code>@​adamchainz</code></a></li> <li><a
  href="https://github.com/carljm"><code>@​carljm</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/dcreager"><code>@​dcreager</code></a></li> <li><a
  href="https://github.com/dhruvmanila"><code>@​dhruvmanila</code></a></li> <li><a
  href="https://github.com/ericmarkmartin"><code>@​ericmarkmartin</code></a></li> <li><a
  href="https://github.com/github-actions"><code>@​github-actions</code></a></li> <li><a
  href="https://github.com/mishamsk"><code>@​mishamsk</code></a></li> <li><a
  href="https://github.com/mtshiba"><code>@​mtshiba</code></a></li> </ul> <!-- raw HTML omitted -->
  </blockquote> <p>... (truncated)</p> </details> <details> <summary>Changelog</summary>
  <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
  changelog</a>.</em></p> <blockquote> <h2>0.9.10</h2> <h3>Preview features</h3> <ul>
  <li>[<code>ruff</code>] Add new rule <code>RUF059</code>: Unused unpacked assignment (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16449">#16449</a>)</li>
  <li>[<code>syntax-errors</code>] Detect assignment expressions before Python 3.8 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16383">#16383</a>)</li>
  <li>[<code>syntax-errors</code>] Named expressions in decorators before Python 3.9 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16386">#16386</a>)</li>
  <li>[<code>syntax-errors</code>] Parenthesized keyword argument names after Python 3.8 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16482">#16482</a>)</li>
  <li>[<code>syntax-errors</code>] Positional-only parameters before Python 3.8 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16481">#16481</a>)</li>
  <li>[<code>syntax-errors</code>] Tuple unpacking in <code>return</code> and <code>yield</code>
  before Python 3.8 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16485">#16485</a>)</li>
  <li>[<code>syntax-errors</code>] Type parameter defaults before Python 3.13 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16447">#16447</a>)</li>
  <li>[<code>syntax-errors</code>] Type parameter lists before Python 3.12 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16479">#16479</a>)</li>
  <li>[<code>syntax-errors</code>] <code>except*</code> before Python 3.11 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16446">#16446</a>)</li>
  <li>[<code>syntax-errors</code>] <code>type</code> statements before Python 3.12 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16478">#16478</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>Escape template filenames in glob patterns in configuration (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16407">#16407</a>)</li>
  <li>[<code>flake8-simplify</code>] Exempt unittest context methods for <code>SIM115</code> rule
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/16439">#16439</a>)</li> <li>Formatter:
  Fix syntax error location in notebooks (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16499">#16499</a>)</li>
  <li>[<code>pyupgrade</code>] Do not offer fix when at least one target is
  <code>global</code>/<code>nonlocal</code> (<code>UP028</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16451">#16451</a>)</li>
  <li>[<code>flake8-builtins</code>] Ignore variables matching module attribute names
  (<code>A001</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16454">#16454</a>)</li>
  <li>[<code>pylint</code>] Convert <code>code</code> keyword argument to a positional argument in
  fix for (<code>PLR1722</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16424">#16424</a>)</li> </ul> <h3>CLI</h3>
  <ul> <li>Move rule code from <code>description</code> to <code>check_name</code> in GitLab output
  serializer (<a href="https://redirect.github.com/astral-sh/ruff/pull/16437">#16437</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>[<code>pydocstyle</code>] Clarify that <code>D417</code> only
  checks docstrings with an arguments section (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16494">#16494</a>)</li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ruff/commit/0dfa810e9aad9a465596768b0211c31dd41d3e73"><code>0dfa810</code></a>
  Bump 0.9.10 (<a href="https://redirect.github.com/astral-sh/ruff/issues/16556">#16556</a>)</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/9cd0cdefd383c5b9ab1f2515b2b7304128f56612"><code>9cd0cde</code></a>
  Assert that formatted code doesn't introduce any new unsupported syntax error...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/05a4c293443ff2f104e4fc6899d8980eea9862ee"><code>05a4c29</code></a>
  print MDTEST_TEST_FILTER value in single-quotes (and escaped) (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16548">#16548</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/b3c884f4f33a81cd08e9ebc13fd0d5a538c8afc7"><code>b3c884f</code></a>
  [syntax-errors] Parenthesized keyword argument names after Python 3.8 (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16482">#16482</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/6c14225c662148d680f7026d52d01de2e47f3938"><code>6c14225</code></a>
  [syntax-errors] Tuple unpacking in <code>return</code> and <code>yield</code> before Python 3.8
  (<a href="https://redirect.github.com/astral-sh/ruff/issues/1">#1</a>...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/0a627ef216bc7a085a4915a8b59ff6440181147b"><code>0a627ef</code></a>
  [red-knot] Never is callable and iterable. Arbitrary attributes can be access...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/a25be4610a1fd3f7e9a4e593da9ccb25e1aae49a"><code>a25be46</code></a>
  Clarify that D417 only checks docstrings with an arguments section (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16494">#16494</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/ce0018c3cb22e39c12d0b88c83953ee215e72552"><code>ce0018c</code></a>
  Add <code>OsSystem</code> support to mdtests (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16518">#16518</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/48f906e06c73fc3ee01dcf3ba312e6a780f5a1cb"><code>48f906e</code></a>
  Add tests for case-sensitive module resolution (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16517">#16517</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/ebd172e732dbc05c7e721c6a441e624873c9ab43"><code>ebd172e</code></a>
  [red-knot] Several failing tests for generics (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16509">#16509</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.9.9...0.9.10">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ruff&package-manager=pip&previous-version=0.9.9&new-version=0.9.10)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump syrupy from 4.8.2 to 4.9.0 ([#572](https://github.com/Twingate/kubernetes-operator/pull/572),
  [`7933a9b`](https://github.com/Twingate/kubernetes-operator/commit/7933a9bba38b5da2a94c5b5ec7e87477348d49b9))

Bumps [syrupy](https://github.com/syrupy-project/syrupy) from 4.8.2 to 4.9.0. <details>
  <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/syrupy-project/syrupy/releases">syrupy's releases</a>.</em></p>
  <blockquote> <h2>v4.9.0</h2> <h1><a
  href="https://github.com/syrupy-project/syrupy/compare/v4.8.3...v4.9.0">4.9.0</a>
  (2025-03-08)</h1> <h3>Bug Fixes</h3> <ul> <li><strong>serializer:</strong> raise TypeError when
  serializing non-byte like object in binary mode (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/951">#951</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/2bd0f54ea0923f4c549209abc40d2eec9b973d65">2bd0f54</a>)</li>
  </ul> <h3>Features</h3> <ul> <li>add --snapshot-ignore-file-extensions argument to support DVC (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/943">#943</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/056cc6e1057f6d1c49b4b609aa09be9f507dd55c">056cc6e</a>)</li>
  <li>add compose_matchers utility for composing 1 or more matchers (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/952">#952</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/157dbecc87fd03ea938c4a7dc194418da43c90a5">157dbec</a>)</li>
  <li>add SingleFileAmberSnapshotExtension as a single-file variant of the default amber extension
  (<a href="https://redirect.github.com/syrupy-project/syrupy/issues/959">#959</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/a753b7a0aa6763a7489da78291bf27b7b5081b74">a753b7a</a>)</li>
  <li>include details about created/updated snapshots in detailed report (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/942">#942</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/25d37ef978cbbd5b034fe394d283e923295b1750">25d37ef</a>)</li>
  </ul> <h2>v4.8.3</h2> <h2><a
  href="https://github.com/syrupy-project/syrupy/compare/v4.8.2...v4.8.3">4.8.3</a>
  (2025-03-08)</h2> <h3>Bug Fixes</h3> <ul> <li>snapshots of deselected parametrized tests wrongly
  marked as unused (<a href="https://redirect.github.com/syrupy-project/syrupy/issues/965">#965</a>)
  (<a
  href="https://github.com/syrupy-project/syrupy/commit/52f3bb2089f6289ef6502486301d56d7b13fdf28">52f3bb2</a>)</li>
  </ul> </blockquote> </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/syrupy-project/syrupy/blob/main/CHANGELOG.md">syrupy's
  changelog</a>.</em></p> <blockquote> <h1><a
  href="https://github.com/syrupy-project/syrupy/compare/v4.8.3...v4.9.0">4.9.0</a>
  (2025-03-08)</h1> <h3>Bug Fixes</h3> <ul> <li><strong>serializer:</strong> raise TypeError when
  serializing non-byte like object in binary mode (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/951">#951</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/2bd0f54ea0923f4c549209abc40d2eec9b973d65">2bd0f54</a>)</li>
  </ul> <h3>Features</h3> <ul> <li>add --snapshot-ignore-file-extensions argument to support DVC (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/943">#943</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/056cc6e1057f6d1c49b4b609aa09be9f507dd55c">056cc6e</a>)</li>
  <li>add compose_matchers utility for composing 1 or more matchers (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/952">#952</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/157dbecc87fd03ea938c4a7dc194418da43c90a5">157dbec</a>)</li>
  <li>add SingleFileAmberSnapshotExtension as a single-file variant of the default amber extension
  (<a href="https://redirect.github.com/syrupy-project/syrupy/issues/959">#959</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/a753b7a0aa6763a7489da78291bf27b7b5081b74">a753b7a</a>)</li>
  <li>include details about created/updated snapshots in detailed report (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/942">#942</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/25d37ef978cbbd5b034fe394d283e923295b1750">25d37ef</a>)</li>
  </ul> <h2><a href="https://github.com/syrupy-project/syrupy/compare/v4.8.2...v4.8.3">4.8.3</a>
  (2025-03-08)</h2> <h3>Bug Fixes</h3> <ul> <li>snapshots of deselected parametrized tests wrongly
  marked as unused (<a href="https://redirect.github.com/syrupy-project/syrupy/issues/965">#965</a>)
  (<a
  href="https://github.com/syrupy-project/syrupy/commit/52f3bb2089f6289ef6502486301d56d7b13fdf28">52f3bb2</a>)</li>
  </ul> </blockquote> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/syrupy-project/syrupy/commit/b2a72f7eb998df9b1eb02d8c1952db5a9e449517"><code>b2a72f7</code></a>
  chore(release): 4.9.0 [skip ci]</li> <li><a
  href="https://github.com/syrupy-project/syrupy/commit/3330c42817cbf4488921270d5ef657ae3358d14d"><code>3330c42</code></a>
  Merge pull request <a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/967">#967</a></li> <li><a
  href="https://github.com/syrupy-project/syrupy/commit/33aca90b2d3cf6cbc3051d6553c7dba9a84a2e7f"><code>33aca90</code></a>
  chore: py3.8 backwards compatibility fix</li> <li><a
  href="https://github.com/syrupy-project/syrupy/commit/a753b7a0aa6763a7489da78291bf27b7b5081b74"><code>a753b7a</code></a>
  feat: add SingleFileAmberSnapshotExtension as a single-file variant of the de...</li> <li><a
  href="https://github.com/syrupy-project/syrupy/commit/157dbecc87fd03ea938c4a7dc194418da43c90a5"><code>157dbec</code></a>
  feat: add compose_matchers utility for composing 1 or more matchers (<a

href="https://redirect.github.com/syrupy-project/syrupy/issues/952">#952</a>)</li> <li><a
  href="https://github.com/syrupy-project/syrupy/commit/2bd0f54ea0923f4c549209abc40d2eec9b973d65"><code>2bd0f54</code></a>
  fix(serializer): raise TypeError when serializing non-byte like object in bin...</li> <li><a
  href="https://github.com/syrupy-project/syrupy/commit/056cc6e1057f6d1c49b4b609aa09be9f507dd55c"><code>056cc6e</code></a>
  feat: add --snapshot-ignore-file-extensions argument to support DVC (<a

href="https://redirect.github.com/syrupy-project/syrupy/issues/943">#943</a>)</li> <li><a
  href="https://github.com/syrupy-project/syrupy/commit/25d37ef978cbbd5b034fe394d283e923295b1750"><code>25d37ef</code></a>
  feat: include details about created/updated snapshots in detailed report (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/942">#942</a>)</li> <li><a
  href="https://github.com/syrupy-project/syrupy/commit/4bc6d13fcf3ea312fac791cfd8826a2ce119a300"><code>4bc6d13</code></a>
  docs: add samylaumonier as a contributor for bug (<a

href="https://redirect.github.com/syrupy-project/syrupy/issues/966">#966</a>)</li> <li><a
  href="https://github.com/syrupy-project/syrupy/commit/39b445f01529f30fa0cbf8c4afc87d56ab01be27"><code>39b445f</code></a>
  chore(release): 4.8.3 [skip ci]</li> <li>Additional commits viewable in <a
  href="https://github.com/syrupy-project/syrupy/compare/v4.8.2...v4.9.0">compare view</a></li>
  </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=syrupy&package-manager=pip&previous-version=4.8.2&new-version=4.9.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump syrupy from 4.9.0 to 4.9.1 ([#584](https://github.com/Twingate/kubernetes-operator/pull/584),
  [`08df2f9`](https://github.com/Twingate/kubernetes-operator/commit/08df2f9f524795a88167b9be0d9ddb9f0723024b))

Bumps [syrupy](https://github.com/syrupy-project/syrupy) from 4.9.0 to 4.9.1. <details>
  <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/syrupy-project/syrupy/releases">syrupy's releases</a>.</em></p>
  <blockquote> <h2>v4.9.1</h2> <h2><a
  href="https://github.com/syrupy-project/syrupy/compare/v4.9.0...v4.9.1">4.9.1</a>
  (2025-03-24)</h2> <h3>Bug Fixes</h3> <ul> <li><strong>serializer:</strong> preserve trailing
  newlines in ambr serialization (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/950">#950</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/5897490e9821156327fe56bc5f7695146e2363a5">5897490</a>)</li>
  <li><strong>serializer:</strong> preserve trailing newlines in ambr serialization (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/950">#950</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/5037477ceece0f2cf861aabd356f4dd07a9eeb71">5037477</a>)</li>
  </ul> </blockquote> </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/syrupy-project/syrupy/blob/main/CHANGELOG.md">syrupy's
  changelog</a>.</em></p> <blockquote> <h2><a
  href="https://github.com/syrupy-project/syrupy/compare/v4.9.0...v4.9.1">4.9.1</a>
  (2025-03-24)</h2> <h3>Bug Fixes</h3> <ul> <li><strong>serializer:</strong> preserve trailing
  newlines in ambr serialization (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/950">#950</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/5897490e9821156327fe56bc5f7695146e2363a5">5897490</a>)</li>
  <li><strong>serializer:</strong> preserve trailing newlines in ambr serialization (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/950">#950</a>) (<a
  href="https://github.com/syrupy-project/syrupy/commit/5037477ceece0f2cf861aabd356f4dd07a9eeb71">5037477</a>)</li>
  </ul> </blockquote> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/syrupy-project/syrupy/commit/431b76d9d9fa4a99a4b6d67aa203ad7c152e97ba"><code>431b76d</code></a>
  chore(release): 4.9.1 [skip ci]</li> <li><a
  href="https://github.com/syrupy-project/syrupy/commit/5897490e9821156327fe56bc5f7695146e2363a5"><code>5897490</code></a>
  fix(serializer): preserve trailing newlines in ambr serialization (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/950">#950</a>)</li> <li><a
  href="https://github.com/syrupy-project/syrupy/commit/5037477ceece0f2cf861aabd356f4dd07a9eeb71"><code>5037477</code></a>
  fix(serializer): preserve trailing newlines in ambr serialization (<a
  href="https://redirect.github.com/syrupy-project/syrupy/issues/950">#950</a>)</li> <li>See full
  diff in <a href="https://github.com/syrupy-project/syrupy/compare/v4.9.0...v4.9.1">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=syrupy&package-manager=pip&previous-version=4.9.0&new-version=4.9.1)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

---------

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

- Bump types-croniter from 5.0.1.20241205 to 5.0.1.20250322
  ([#585](https://github.com/Twingate/kubernetes-operator/pull/585),
  [`bb7d493`](https://github.com/Twingate/kubernetes-operator/commit/bb7d493a66de0c6ae489284a673358f1b4572d2f))

Bumps [types-croniter](https://github.com/python/typeshed) from 5.0.1.20241205 to 5.0.1.20250322.
  <details> <summary>Commits</summary> <ul> <li>See full diff in <a
  href="https://github.com/python/typeshed/commits">compare view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=types-croniter&package-manager=pip&previous-version=5.0.1.20241205&new-version=5.0.1.20250322)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-pyyaml from 6.0.12.20241230 to 6.0.12.20250326
  ([#588](https://github.com/Twingate/kubernetes-operator/pull/588),
  [`c49fd2c`](https://github.com/Twingate/kubernetes-operator/commit/c49fd2cfba092a9b8facd12ca70b7b71b892accf))

Bumps [types-pyyaml](https://github.com/python/typeshed) from 6.0.12.20241230 to 6.0.12.20250326.
  <details> <summary>Commits</summary> <ul> <li>See full diff in <a
  href="https://github.com/python/typeshed/commits">compare view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=types-pyyaml&package-manager=pip&previous-version=6.0.12.20241230&new-version=6.0.12.20250326)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.32.0.20241016 to 2.32.0.20250301
  ([#564](https://github.com/Twingate/kubernetes-operator/pull/564),
  [`93ee2e8`](https://github.com/Twingate/kubernetes-operator/commit/93ee2e891ec032093e137afbbf6fb0779d578113))

Bumps [types-requests](https://github.com/python/typeshed) from 2.32.0.20241016 to 2.32.0.20250301.
  <details> <summary>Commits</summary> <ul> <li>See full diff in <a
  href="https://github.com/python/typeshed/commits">compare view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=types-requests&package-manager=pip&previous-version=2.32.0.20241016&new-version=2.32.0.20250301)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.32.0.20250301 to 2.32.0.20250306
  ([#567](https://github.com/Twingate/kubernetes-operator/pull/567),
  [`ba28c63`](https://github.com/Twingate/kubernetes-operator/commit/ba28c63387a0b11da0555bde87b975ac91695001))

Bumps [types-requests](https://github.com/python/typeshed) from 2.32.0.20250301 to 2.32.0.20250306.
  <details> <summary>Commits</summary> <ul> <li>See full diff in <a
  href="https://github.com/python/typeshed/commits">compare view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=types-requests&package-manager=pip&previous-version=2.32.0.20250301&new-version=2.32.0.20250306)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot merge` will merge this PR after your CI passes on it - `@dependabot squash and
  merge` will squash and merge this PR after your CI passes on it - `@dependabot cancel merge` will
  cancel a previously requested merge and block automerging - `@dependabot reopen` will reopen this
  PR if it is closed - `@dependabot close` will close this PR and stop Dependabot recreating it. You
  can achieve the same result by closing it manually - `@dependabot show <dependency name> ignore
  conditions` will show all of the ignore conditions of the specified dependency - `@dependabot
  ignore this major version` will close this PR and stop Dependabot creating any more for this major
  version (unless you reopen the PR or upgrade to it yourself) - `@dependabot ignore this minor
  version` will close this PR and stop Dependabot creating any more for this minor version (unless
  you reopen the PR or upgrade to it yourself) - `@dependabot ignore this dependency` will close
  this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or
  upgrade to it yourself)

</details>

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump tzdata from 2023.3 to 2025.2
  ([`5436813`](https://github.com/Twingate/kubernetes-operator/commit/5436813d8994667d8c3c45b75b15ab3a081d6dfd))

- Fix dockerfile “AS” to uppercase
  ([`1a17ce6`](https://github.com/Twingate/kubernetes-operator/commit/1a17ce61fcdfc1065ced8448929fa24c29b046fc))

### Documentation

- Fix typo 'closing' → 'cloning' in Helm installation section
  ([#575](https://github.com/Twingate/kubernetes-operator/pull/575),
  [`5fb8062`](https://github.com/Twingate/kubernetes-operator/commit/5fb8062b26edd9856b6e75b1376bd69a544798c8))

**Changes** This PR fixes a small typo in the README.md file:

- "Helm by **closing** the git repository" → "Helm by **cloning** the git repository" - Ensures
  clarity in the installation instructions for users installing via Helm.

**Notes** N/A (No breaking changes or alternative approaches considered.)

### Features

- Support for removing annotation from service + integration tests
  ([#534](https://github.com/Twingate/kubernetes-operator/pull/534),
  [`e6cd068`](https://github.com/Twingate/kubernetes-operator/commit/e6cd06849d5e958be082c97706e25a04374272ec))

- **crds**: Add categories to CRDs and fix indentation for shortNames to enhance organization and
  readability in Kubernetes resources
  ([#579](https://github.com/Twingate/kubernetes-operator/pull/579),
  [`f8255f1`](https://github.com/Twingate/kubernetes-operator/commit/f8255f16cd512aa823def435bb73aa04c1284098))

## Changes

Added category to our objects so that they appear when doing `kubectl get all` but also added a
  specific twingate category so all our objects appear on `kubectl get twingate`

Example: ``` ➜ kubectl get twingate NAME ID DISPLAY NAME AGE
  twingateconnector.twingate.com/my-connector-auto-updating-image Q29ubmVjdG9yOjk3MDU1OQ==
  nondescript-jackrabbit 18m twingateconnector.twingate.com/my-connector-fixed-image
  Q29ubmVjdG9yOjk3MDU2MA== icy-orca 18m

NAME ID DISPLAY NAME AGE twingategroup.twingate.com/example R3JvdXA6MzA1NDM5NA== Example Group 18m

NAME CREATE STATUS SYNC STATUS AGE twingateresourceaccess.twingate.com/my-twingate-access 2m51s

NAME ID DISPLAY NAME ADDRESS ALIAS AGE twingateresource.twingate.com/my-service-resource
  UmVzb3VyY2U6MzA3ODgwNQ== my-service-resource my-service.default.svc.cluster.local myapp.internal
  9d twingateresource.twingate.com/my-twingate-resource UmVzb3VyY2U6MzA3ODgwNA== My K8S Resource
  demo updated! my.default.cluster.local mine.local 9d ```


## v0.17.0 (2025-02-25)

### Chores

- Bump azure/setup-helm from 4.2.0 to 4.3.0
  ([#552](https://github.com/Twingate/kubernetes-operator/pull/552),
  [`4213684`](https://github.com/Twingate/kubernetes-operator/commit/4213684cbf49e17f7f913954dce892d8cfc2433e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump bandit from 1.8.2 to 1.8.3 ([#547](https://github.com/Twingate/kubernetes-operator/pull/547),
  [`89411ed`](https://github.com/Twingate/kubernetes-operator/commit/89411ed0c72912ead747f87138358ffee418c7f0))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump danger/danger-js from 12.3.3 to 12.3.4
  ([#545](https://github.com/Twingate/kubernetes-operator/pull/545),
  [`1241bf6`](https://github.com/Twingate/kubernetes-operator/commit/1241bf66bf1986a15fdfdcfc30b57ae665d1412b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump factory-boy from 3.3.1 to 3.3.3
  ([#536](https://github.com/Twingate/kubernetes-operator/pull/536),
  [`aef79b1`](https://github.com/Twingate/kubernetes-operator/commit/aef79b1dcfeb54936d7b0980d3855770f125c49d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump github.com/gruntwork-io/terratest from 0.48.1 to 0.48.2
  ([#537](https://github.com/Twingate/kubernetes-operator/pull/537),
  [`1c81b05`](https://github.com/Twingate/kubernetes-operator/commit/1c81b05f3cbe87cdb680e1461428a2e2983fbd49))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google-cloud-artifact-registry from 1.14.0 to 1.15.0
  ([#546](https://github.com/Twingate/kubernetes-operator/pull/546),
  [`06eecb6`](https://github.com/Twingate/kubernetes-operator/commit/06eecb62aee4edfecb2bb25f9e989d87b1da2292))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google-cloud-artifact-registry from 1.15.0 to 1.15.1
  ([#553](https://github.com/Twingate/kubernetes-operator/pull/553),
  [`19f687b`](https://github.com/Twingate/kubernetes-operator/commit/19f687b00c177c1d7455e4d7f6242f642797e117))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump gql from 3.5.0 to 3.5.1 ([#550](https://github.com/Twingate/kubernetes-operator/pull/550),
  [`6d6a860`](https://github.com/Twingate/kubernetes-operator/commit/6d6a860f11fc037bdc49f28a823e6ef77a72468b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump kubernetes from 32.0.0 to 32.0.1
  ([#549](https://github.com/Twingate/kubernetes-operator/pull/549),
  [`fe454e9`](https://github.com/Twingate/kubernetes-operator/commit/fe454e92ee0c601c66c4a677a848c00990b3f2b8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump mypy from 1.14.1 to 1.15.0 ([#538](https://github.com/Twingate/kubernetes-operator/pull/538),
  [`669bf99`](https://github.com/Twingate/kubernetes-operator/commit/669bf99c77f156985c9f0acecf6ee01b77df0cc2))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ncipollo/release-action from 1.15.0 to 1.16.0
  ([#557](https://github.com/Twingate/kubernetes-operator/pull/557),
  [`f07184f`](https://github.com/Twingate/kubernetes-operator/commit/f07184f5233b88ac2efe8f2adb766e0942ea10d7))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.7.1 to 2.8.0
  ([#554](https://github.com/Twingate/kubernetes-operator/pull/554),
  [`b3109d0`](https://github.com/Twingate/kubernetes-operator/commit/b3109d0cc222114c3f50625dd5798c82c8fe7773))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest-datadir from 1.5.0 to 1.6.1
  ([#541](https://github.com/Twingate/kubernetes-operator/pull/541),
  [`0f1696a`](https://github.com/Twingate/kubernetes-operator/commit/0f1696a358fb20200cc5da47d87f536d48dd682f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.17.0 to 9.18.0
  ([#539](https://github.com/Twingate/kubernetes-operator/pull/539),
  [`7c8a2b5`](https://github.com/Twingate/kubernetes-operator/commit/7c8a2b5d1b9e68267446917e3c467093d721c2fe))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.18.0 to 9.19.0
  ([#543](https://github.com/Twingate/kubernetes-operator/pull/543),
  [`2db1f42`](https://github.com/Twingate/kubernetes-operator/commit/2db1f426b5bf96eb0666c28f19de43188f326303))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.19.0 to 9.19.1
  ([#544](https://github.com/Twingate/kubernetes-operator/pull/544),
  [`efb99d0`](https://github.com/Twingate/kubernetes-operator/commit/efb99d0bdb1e27163ceddadeb3c1ee7910a7575a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.19.1 to 9.20.0
  ([#548](https://github.com/Twingate/kubernetes-operator/pull/548),
  [`9bfc8e5`](https://github.com/Twingate/kubernetes-operator/commit/9bfc8e5001f499f1da29b30c0a74fcf2ed90ac26))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.20.0 to 9.21.0
  ([#558](https://github.com/Twingate/kubernetes-operator/pull/558),
  [`c425b4d`](https://github.com/Twingate/kubernetes-operator/commit/c425b4d0df93fb6a85a4278772d78f9878e57cd8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.9.3 to 0.9.4 ([#535](https://github.com/Twingate/kubernetes-operator/pull/535),
  [`141ec37`](https://github.com/Twingate/kubernetes-operator/commit/141ec376096941f3a7d4672e76bdb846535006d9))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.9.4 to 0.9.5 ([#540](https://github.com/Twingate/kubernetes-operator/pull/540),
  [`98bc251`](https://github.com/Twingate/kubernetes-operator/commit/98bc25126d255b4277e94c427b3eb98d0635683e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.9.5 to 0.9.6 ([#542](https://github.com/Twingate/kubernetes-operator/pull/542),
  [`d3e48cf`](https://github.com/Twingate/kubernetes-operator/commit/d3e48cf458115993dd820932eb35d487122f7792))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.9.6 to 0.9.7 ([#551](https://github.com/Twingate/kubernetes-operator/pull/551),
  [`1f9d351`](https://github.com/Twingate/kubernetes-operator/commit/1f9d351b4abe7cba8d56bdd13ed2e561356bfc0f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump syrupy from 4.8.1 to 4.8.2 ([#555](https://github.com/Twingate/kubernetes-operator/pull/555),
  [`7590c10`](https://github.com/Twingate/kubernetes-operator/commit/7590c10ec9a5a5fea90565c570eb89aa9f9d89bc))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Update local dev version of Python to 3.12.9
  ([`a8eb289`](https://github.com/Twingate/kubernetes-operator/commit/a8eb289dd36dbfe8bf3846824f0760f0ca581ddb))

### Documentation

- Improve TwingateResourceAccess CRD descriptions
  ([#559](https://github.com/Twingate/kubernetes-operator/pull/559),
  [`636670d`](https://github.com/Twingate/kubernetes-operator/commit/636670d6ac06f2e9f01f450ae8222325b2eccff7))

## Changes

Added\improved TwingateResourceAccess CRD descriptions

### Features

- Add app-version to chart when releasing prod
  ([#560](https://github.com/Twingate/kubernetes-operator/pull/560),
  [`d6302dc`](https://github.com/Twingate/kubernetes-operator/commit/d6302dc81d7932396b3e6d31487ea527f5b7f0f1))

## Related Tickets & Documents

- Issue: #556

## Changes

Add appVersion to chart when releasing prod


## v0.16.2 (2025-01-28)

### Bug Fixes

- Service annotations update not working
  ([#531](https://github.com/Twingate/kubernetes-operator/pull/531),
  [`48fa93c`](https://github.com/Twingate/kubernetes-operator/commit/48fa93c36331a7a0ec77c48a7ac9116578934460))

### Chores

- Bump bandit from 1.8.0 to 1.8.2 ([#515](https://github.com/Twingate/kubernetes-operator/pull/515),
  [`8e83903`](https://github.com/Twingate/kubernetes-operator/commit/8e8390384ccd6e7573b04b4216e77413552a0f93))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump golang.org/x/net from 0.31.0 to 0.33.0
  ([#523](https://github.com/Twingate/kubernetes-operator/pull/523),
  [`0ff77c5`](https://github.com/Twingate/kubernetes-operator/commit/0ff77c5abc1b74a1eda686b3588aa547edb371f2))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump kubernetes from 31.0.0 to 32.0.0
  ([#527](https://github.com/Twingate/kubernetes-operator/pull/527),
  [`91c5042`](https://github.com/Twingate/kubernetes-operator/commit/91c504295746b2133f4fad6f5d6df74fc2fcf8b4))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ncipollo/release-action from 1.14.0 to 1.15.0
  ([#511](https://github.com/Twingate/kubernetes-operator/pull/511),
  [`5e7724e`](https://github.com/Twingate/kubernetes-operator/commit/5e7724eabfb954eddfb802ff89051907420f5666))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.13 to 3.10.14
  ([#508](https://github.com/Twingate/kubernetes-operator/pull/508),
  [`8255523`](https://github.com/Twingate/kubernetes-operator/commit/8255523d8733a716f9b4222646e711f15350f5d2))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.14 to 3.10.15
  ([#524](https://github.com/Twingate/kubernetes-operator/pull/524),
  [`0744ad8`](https://github.com/Twingate/kubernetes-operator/commit/0744ad80ee1f87bf8102a7fdf44e0a36afdd9d9a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pre-commit from 4.0.1 to 4.1.0
  ([#525](https://github.com/Twingate/kubernetes-operator/pull/525),
  [`bddea4f`](https://github.com/Twingate/kubernetes-operator/commit/bddea4f8d00fd9ccce96eb5cf5592498531e457d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.10.4 to 2.10.5
  ([#510](https://github.com/Twingate/kubernetes-operator/pull/510),
  [`fb33861`](https://github.com/Twingate/kubernetes-operator/commit/fb33861aa308e9924b62b0854b9e48e3e55bbb0c))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.10.5 to 2.10.6
  ([#529](https://github.com/Twingate/kubernetes-operator/pull/529),
  [`5d3d000`](https://github.com/Twingate/kubernetes-operator/commit/5d3d000c6c4a8edb4542e5da8bc48755c4162391))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.15.2 to 9.16.1
  ([#514](https://github.com/Twingate/kubernetes-operator/pull/514),
  [`b356c73`](https://github.com/Twingate/kubernetes-operator/commit/b356c73ebb8fea8512c053456d0ce8858c27692f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.16.1 to 9.17.0
  ([#532](https://github.com/Twingate/kubernetes-operator/pull/532),
  [`c5c6c83`](https://github.com/Twingate/kubernetes-operator/commit/c5c6c83b6db2a64da4826cb45488ed70097af996))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump responses from 0.25.3 to 0.25.5
  ([#516](https://github.com/Twingate/kubernetes-operator/pull/516),
  [`7d89215`](https://github.com/Twingate/kubernetes-operator/commit/7d892152cc0555c23217eb5eb18ff1b88d2c67c9))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump responses from 0.25.5 to 0.25.6
  ([#521](https://github.com/Twingate/kubernetes-operator/pull/521),
  [`5aabf03`](https://github.com/Twingate/kubernetes-operator/commit/5aabf039adce0dde366017ab6a13559b8cf1a780))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.8.6 to 0.9.1 ([#513](https://github.com/Twingate/kubernetes-operator/pull/513),
  [`13528a4`](https://github.com/Twingate/kubernetes-operator/commit/13528a45e30c1b5e245d4c05a7958791f5bd1b31))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

- Bump ruff from 0.9.1 to 0.9.2 ([#522](https://github.com/Twingate/kubernetes-operator/pull/522),
  [`642e3e5`](https://github.com/Twingate/kubernetes-operator/commit/642e3e5c72f5bca5038692ab67c3050b061986df))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.9.2 to 0.9.3 ([#528](https://github.com/Twingate/kubernetes-operator/pull/528),
  [`86da11b`](https://github.com/Twingate/kubernetes-operator/commit/86da11b2d837f53f99b09a430afe2581c9da03b3))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump syrupy from 4.8.0 to 4.8.1 ([#512](https://github.com/Twingate/kubernetes-operator/pull/512),
  [`edb984a`](https://github.com/Twingate/kubernetes-operator/commit/edb984a9c4bfa546fd801d7535bba1edd7e0a9a6))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump virtualenv from 20.24.5 to 20.26.6
  ([#517](https://github.com/Twingate/kubernetes-operator/pull/517),
  [`37adbf5`](https://github.com/Twingate/kubernetes-operator/commit/37adbf5933a16d680102b4e5003213fe723fd194))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Remove `isort` and use `ruff` instead
  ([#518](https://github.com/Twingate/kubernetes-operator/pull/518),
  [`5a754da`](https://github.com/Twingate/kubernetes-operator/commit/5a754da22cda2b2457a3f006d7694d50284c7cdd))

- Remove autoflake and use Ruff instead + Extra Ruff rules
  ([#519](https://github.com/Twingate/kubernetes-operator/pull/519),
  [`3ec387c`](https://github.com/Twingate/kubernetes-operator/commit/3ec387c4fad3239ce0de4e36cc7d9dbf170fdad9))

- Upgrade Poetry to 1.8.5 -> 2.0.1
  ([#520](https://github.com/Twingate/kubernetes-operator/pull/520),
  [`32c12cb`](https://github.com/Twingate/kubernetes-operator/commit/32c12cbfca55673fd85408e6d967b59dcb94333d))


## v0.16.1 (2025-01-06)

### Bug Fixes

- Ensure Proper Type Parsing in Kopf Settings
  ([#504](https://github.com/Twingate/kubernetes-operator/pull/504),
  [`18ac8fe`](https://github.com/Twingate/kubernetes-operator/commit/18ac8fe6e24c1e3fe7bab6754fa36b058d63562b))

Co-authored-by: Eran Kampf <205185+ekampf@users.noreply.github.com>

- Make integration tests more stable
  ([#506](https://github.com/Twingate/kubernetes-operator/pull/506),
  [`ffa70d4`](https://github.com/Twingate/kubernetes-operator/commit/ffa70d461b9340eafa8a483c133d0799afaf7b3f))

### Chores

- Bump mypy from 1.14.0 to 1.14.1 ([#503](https://github.com/Twingate/kubernetes-operator/pull/503),
  [`891239e`](https://github.com/Twingate/kubernetes-operator/commit/891239eb0973916d9a4c30711a5f7d1d6d94894e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.12 to 3.10.13
  ([#501](https://github.com/Twingate/kubernetes-operator/pull/501),
  [`5199b1f`](https://github.com/Twingate/kubernetes-operator/commit/5199b1f88be9dc9df7c881af7b220b69505724a7))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.7.0 to 2.7.1
  ([#502](https://github.com/Twingate/kubernetes-operator/pull/502),
  [`868e2e3`](https://github.com/Twingate/kubernetes-operator/commit/868e2e3532fd65bfe43613338715a9457df40580))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.8.4 to 0.8.5 ([#505](https://github.com/Twingate/kubernetes-operator/pull/505),
  [`31f694f`](https://github.com/Twingate/kubernetes-operator/commit/31f694faa3acc1f1cd6eeb9c4990fe22e05ffc0e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.8.5 to 0.8.6 ([#507](https://github.com/Twingate/kubernetes-operator/pull/507),
  [`98892cb`](https://github.com/Twingate/kubernetes-operator/commit/98892cb8ada9425be86bb174ba5087afcac0a721))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>


## v0.16.0 (2024-12-26)

### Features

- Helm chart - Add `existingRemoteNetworkIdSecret`
  ([#500](https://github.com/Twingate/kubernetes-operator/pull/500),
  [`5061de0`](https://github.com/Twingate/kubernetes-operator/commit/5061de07afb2fcd13af63d0295d1c47d135e0d7b))


## v0.15.0 (2024-12-23)

### Chores

- Bump croniter from 5.0.1 to 6.0.0
  ([#494](https://github.com/Twingate/kubernetes-operator/pull/494),
  [`d9944a5`](https://github.com/Twingate/kubernetes-operator/commit/d9944a5fc43e9d6bd1ca1ac00a52dcf555636e05))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump github.com/gruntwork-io/terratest from 0.48.0 to 0.48.1
  ([#493](https://github.com/Twingate/kubernetes-operator/pull/493),
  [`a4deb4d`](https://github.com/Twingate/kubernetes-operator/commit/a4deb4dafbff8eedbcec55cc61a2d723a6760a1e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump jinja2 from 3.1.4 to 3.1.5 ([#499](https://github.com/Twingate/kubernetes-operator/pull/499),
  [`05913e3`](https://github.com/Twingate/kubernetes-operator/commit/05913e3cc3aea2b814c8c1e656d64a743d36597c))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump mypy from 1.13.0 to 1.14.0 ([#498](https://github.com/Twingate/kubernetes-operator/pull/498),
  [`e8adb5d`](https://github.com/Twingate/kubernetes-operator/commit/e8adb5d597f7df70dc4db1168a5fdb4a8f9c11e2))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.10.3 to 2.10.4
  ([#496](https://github.com/Twingate/kubernetes-operator/pull/496),
  [`519ee4f`](https://github.com/Twingate/kubernetes-operator/commit/519ee4f31c0cefa14de0d381c582741efd489d3d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pyupgrade from 3.19.0 to 3.19.1
  ([#492](https://github.com/Twingate/kubernetes-operator/pull/492),
  [`ffbca7f`](https://github.com/Twingate/kubernetes-operator/commit/ffbca7fad06a2347b9517c8330d34c23a8d5b292))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.8.3 to 0.8.4 ([#497](https://github.com/Twingate/kubernetes-operator/pull/497),
  [`5b03229`](https://github.com/Twingate/kubernetes-operator/commit/5b03229ba0c7f843af7213070c4a6c242ed1c26a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Fix typo in release script
  ([`8e31713`](https://github.com/Twingate/kubernetes-operator/commit/8e3171375aee8724df0490ee076b58c216eb9d09))

- Switch to markdownlint-cli
  ([`4468f96`](https://github.com/Twingate/kubernetes-operator/commit/4468f96f2512d5850170c335258a36ef408c4723))

Easier to configure

- Upgrade Poetry to 1.8.5
  ([`e7fd65d`](https://github.com/Twingate/kubernetes-operator/commit/e7fd65d4c893a59dca02d64fad61881f093d6bb8))

- Upgrade Poetry to 1.8.5 in CI
  ([`36841ed`](https://github.com/Twingate/kubernetes-operator/commit/36841ed137e506208a85e618b18e8a9eb123fa5c))

### Features

- Publish versioned helm chart to GitHub OCI reposiotry
  ([#479](https://github.com/Twingate/kubernetes-operator/pull/479),
  [`971ba7e`](https://github.com/Twingate/kubernetes-operator/commit/971ba7ee9703202fb2cd632299ca5025c267779a))


## v0.14.1 (2024-12-16)

### Bug Fixes

- Allow extra env vars in the operator's Chart
  ([#491](https://github.com/Twingate/kubernetes-operator/pull/491),
  [`81bf885`](https://github.com/Twingate/kubernetes-operator/commit/81bf885b6c5c27dc075dab8b1f932f36170bff9c))


## v0.14.0 (2024-12-16)

### Chores

- Bump github.com/gruntwork-io/terratest from 0.47.2 to 0.48.0
  ([#480](https://github.com/Twingate/kubernetes-operator/pull/480),
  [`16dba29`](https://github.com/Twingate/kubernetes-operator/commit/16dba292e42961e6347df224ec36e2efb2a360ab))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump golang.org/x/crypto from 0.21.0 to 0.31.0
  ([#482](https://github.com/Twingate/kubernetes-operator/pull/482),
  [`48b5ad1`](https://github.com/Twingate/kubernetes-operator/commit/48b5ad113fb5167d7c692cebdbe2c14bdc53ca5f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google-cloud-artifact-registry from 1.13.1 to 1.14.0
  ([#484](https://github.com/Twingate/kubernetes-operator/pull/484),
  [`baeb563`](https://github.com/Twingate/kubernetes-operator/commit/baeb563f2fa9dc64fb69c78f5f3a2345ba3b0c12))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump kopf from 1.37.3 to 1.37.4 ([#488](https://github.com/Twingate/kubernetes-operator/pull/488),
  [`f17436f`](https://github.com/Twingate/kubernetes-operator/commit/f17436fbd595fea4dc579acd3ded66bfad588ccb))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.6.1 to 2.7.0
  ([#483](https://github.com/Twingate/kubernetes-operator/pull/483),
  [`f43c3c3`](https://github.com/Twingate/kubernetes-operator/commit/f43c3c3f050ea5ab143fa6badc559f546e9ebda8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

- Bump python-semantic-release from 9.15.1 to 9.15.2
  ([#489](https://github.com/Twingate/kubernetes-operator/pull/489),
  [`d911b83`](https://github.com/Twingate/kubernetes-operator/commit/d911b83ca3ad6240a56544033ab8cebbcb1d9d55))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.8.2 to 0.8.3 ([#485](https://github.com/Twingate/kubernetes-operator/pull/485),
  [`8a600a0`](https://github.com/Twingate/kubernetes-operator/commit/8a600a09a7e16cb5b04d43eb807f3c8770a8be25))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Fix README markdownlint warnings
  ([`c623d90`](https://github.com/Twingate/kubernetes-operator/commit/c623d9030e3266ab3ca4e141aee7d25079d3c228))

### Features

- Allow using a pull thru docker cache with the imagepolicy schedule
  ([#477](https://github.com/Twingate/kubernetes-operator/pull/477),
  [`81fdb30`](https://github.com/Twingate/kubernetes-operator/commit/81fdb30022b8b7185c7148607b61dd1b7c5bb755))

Co-authored-by: Lior Rozner <1411811+liorr@users.noreply.github.com>

- Enable Configuration of Kopf Watch Settings via Environment Variables
  ([#487](https://github.com/Twingate/kubernetes-operator/pull/487),
  [`3da4225`](https://github.com/Twingate/kubernetes-operator/commit/3da4225865e767fe8ca74477f477bf2b3ca8fc02))

Co-authored-by: Eran Kampf <205185+ekampf@users.noreply.github.com>


## v0.13.0 (2024-12-06)

### Bug Fixes

- Update Chart version
  ([`0e0efe5`](https://github.com/Twingate/kubernetes-operator/commit/0e0efe5e9a858497c085c5f6ce3788ad43a3d934))

We updated CRDs without the chart version

### Chores

- Bump aiohttp from 3.10.2 to 3.10.11
  ([#462](https://github.com/Twingate/kubernetes-operator/pull/462),
  [`efddeee`](https://github.com/Twingate/kubernetes-operator/commit/efddeee21cb4557e7ac00c0a39e433a62c2b17c0))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump bandit from 1.7.10 to 1.8.0
  ([#468](https://github.com/Twingate/kubernetes-operator/pull/468),
  [`5f9af7f`](https://github.com/Twingate/kubernetes-operator/commit/5f9af7f1ef1dfcb9e3d5f2351a83afbe614b5f30))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google-cloud-artifact-registry from 1.13.0 to 1.13.1
  ([#459](https://github.com/Twingate/kubernetes-operator/pull/459),
  [`b2e5621`](https://github.com/Twingate/kubernetes-operator/commit/b2e5621390e62e9fe2ed5c562662f9643d6c4b22))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump kopf from 1.37.2 to 1.37.3 ([#460](https://github.com/Twingate/kubernetes-operator/pull/460),
  [`1261c0f`](https://github.com/Twingate/kubernetes-operator/commit/1261c0f0680bf9c8a0d13af81ae78f86a33981fe))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.11 to 3.10.12
  ([#465](https://github.com/Twingate/kubernetes-operator/pull/465),
  [`c1aa7cc`](https://github.com/Twingate/kubernetes-operator/commit/c1aa7ccbd3f380aec0a673ab83933812e489b991))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.10.0 to 2.10.2
  ([#467](https://github.com/Twingate/kubernetes-operator/pull/467),
  [`f889dcb`](https://github.com/Twingate/kubernetes-operator/commit/f889dcb1e09052388672bfcddb58a3c1fa6366aa))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.10.2 to 2.10.3
  ([#473](https://github.com/Twingate/kubernetes-operator/pull/473),
  [`ba5c4cb`](https://github.com/Twingate/kubernetes-operator/commit/ba5c4cb88abb7e6215fd17177c680e586f6cfd57))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.9.2 to 2.10.0
  ([#461](https://github.com/Twingate/kubernetes-operator/pull/461),
  [`c2f4be3`](https://github.com/Twingate/kubernetes-operator/commit/c2f4be3bb3e805e06705c8b95e3c374aacf49754))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 8.3.3 to 8.3.4 ([#470](https://github.com/Twingate/kubernetes-operator/pull/470),
  [`42a9aa2`](https://github.com/Twingate/kubernetes-operator/commit/42a9aa239ce3f9545c77561a54d7aed58bc1364b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.12.1 to 9.12.2
  ([#454](https://github.com/Twingate/kubernetes-operator/pull/454),
  [`dfff3dd`](https://github.com/Twingate/kubernetes-operator/commit/dfff3dd3121dda7cab9ee67f970e49eec55085d8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.12.2 to 9.14.0
  ([#457](https://github.com/Twingate/kubernetes-operator/pull/457),
  [`527a398`](https://github.com/Twingate/kubernetes-operator/commit/527a398ae04297ebc6c9b70d1e2db83fd460a617))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.14.0 to 9.15.0
  ([#471](https://github.com/Twingate/kubernetes-operator/pull/471),
  [`32a804f`](https://github.com/Twingate/kubernetes-operator/commit/32a804f7990b86a023041384e7215166516a3b8e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.15.0 to 9.15.1
  ([#472](https://github.com/Twingate/kubernetes-operator/pull/472),
  [`422fae7`](https://github.com/Twingate/kubernetes-operator/commit/422fae7dde116b7a78d9d91b881b0b4f6bc4f0c9))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.7.2 to 0.7.3 ([#455](https://github.com/Twingate/kubernetes-operator/pull/455),
  [`5ddf682`](https://github.com/Twingate/kubernetes-operator/commit/5ddf682d023f2b38cf7ea98e9ddd34607f1a2a56))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

Co-authored-by: Eran Kampf <205185+ekampf@users.noreply.github.com>

- Bump ruff from 0.7.3 to 0.7.4 ([#458](https://github.com/Twingate/kubernetes-operator/pull/458),
  [`d45896f`](https://github.com/Twingate/kubernetes-operator/commit/d45896fb710f65f66252c3522ba1d233ddc11cf9))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.7.4 to 0.8.1 ([#469](https://github.com/Twingate/kubernetes-operator/pull/469),
  [`66f49ff`](https://github.com/Twingate/kubernetes-operator/commit/66f49ff436b35be5df0c8cb9462c1087deb48d6b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

- Bump ruff from 0.8.1 to 0.8.2 ([#476](https://github.com/Twingate/kubernetes-operator/pull/476),
  [`15ea2ed`](https://github.com/Twingate/kubernetes-operator/commit/15ea2edc331cc6cc3f0ba0176676abdf9986639b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump syrupy from 4.7.2 to 4.8.0 ([#466](https://github.com/Twingate/kubernetes-operator/pull/466),
  [`33127ba`](https://github.com/Twingate/kubernetes-operator/commit/33127ba1c5398930c8e96f1624ebf797b748df39))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-croniter from 4.0.0.20241030 to 5.0.1.20241205
  ([#475](https://github.com/Twingate/kubernetes-operator/pull/475),
  [`0fd2aad`](https://github.com/Twingate/kubernetes-operator/commit/0fd2aad9fa28b274d4fa57eda68f97f22bd31148))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Upgrade local asdf Python requirement to latest Python 3.11
  ([`0d49e08`](https://github.com/Twingate/kubernetes-operator/commit/0d49e08bd94ad1aef84a5685958bf22ccbab726c))

### Features

- Allow adding custom labels to the TwingateConnector pod
  ([#474](https://github.com/Twingate/kubernetes-operator/pull/474),
  [`187fb1a`](https://github.com/Twingate/kubernetes-operator/commit/187fb1a7a55999fd12e6cf32f287f798b3bfa1ab))

- Upgrade to Python 3.12.8 ([#478](https://github.com/Twingate/kubernetes-operator/pull/478),
  [`3c5cb73`](https://github.com/Twingate/kubernetes-operator/commit/3c5cb73e390abe0fdc3a243885aa3ce601e485ec))


## v0.12.1 (2024-11-08)

### Chores

- Bump python-semantic-release from 9.12.0 to 9.12.1
  ([#453](https://github.com/Twingate/kubernetes-operator/pull/453),
  [`40cfedc`](https://github.com/Twingate/kubernetes-operator/commit/40cfedc570d263351a1e8d0c865749e74fcadfd4))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>


## v0.12.0 (2024-11-04)

### Bug Fixes

- Twingateresourceaccess deletion fail if resource has been deleted
  ([#420](https://github.com/Twingate/kubernetes-operator/pull/420),
  [`2ede60f`](https://github.com/Twingate/kubernetes-operator/commit/2ede60fbe9f2443151e4f71d1ab5bc6f5539e0e2))

### Chores

- Bump aiohttp from 3.9.4 to 3.10.2
  ([#384](https://github.com/Twingate/kubernetes-operator/pull/384),
  [`619aa3c`](https://github.com/Twingate/kubernetes-operator/commit/619aa3cf8069d6d1b432594aa70c62535330d264))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump bandit from 1.7.9 to 1.7.10
  ([#414](https://github.com/Twingate/kubernetes-operator/pull/414),
  [`e2bac71`](https://github.com/Twingate/kubernetes-operator/commit/e2bac71ae1356c6abe6155dda5f3dffa1fa5d133))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump certifi from 2023.7.22 to 2024.7.4
  ([#348](https://github.com/Twingate/kubernetes-operator/pull/348),
  [`ee89e41`](https://github.com/Twingate/kubernetes-operator/commit/ee89e419a7801cfeefd8a631e1685e4b944ef487))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump croniter from 2.0.5 to 2.0.7
  ([#357](https://github.com/Twingate/kubernetes-operator/pull/357),
  [`9b72cec`](https://github.com/Twingate/kubernetes-operator/commit/9b72cec553f6f03103e73ed151a08a760c9426c7))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump croniter from 2.0.7 to 3.0.0
  ([#365](https://github.com/Twingate/kubernetes-operator/pull/365),
  [`f033f9c`](https://github.com/Twingate/kubernetes-operator/commit/f033f9c587636aa3f4750a66d6c5ffa951da521d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump croniter from 3.0.0 to 3.0.1
  ([#368](https://github.com/Twingate/kubernetes-operator/pull/368),
  [`aa7c32d`](https://github.com/Twingate/kubernetes-operator/commit/aa7c32d3764775ed03860247a81871497781a4bc))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump croniter from 3.0.1 to 3.0.3
  ([#371](https://github.com/Twingate/kubernetes-operator/pull/371),
  [`c5715cf`](https://github.com/Twingate/kubernetes-operator/commit/c5715cf85e8d457699870923dd61cadba94acb5f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump croniter from 3.0.3 to 3.0.4
  ([#442](https://github.com/Twingate/kubernetes-operator/pull/442),
  [`5dfadee`](https://github.com/Twingate/kubernetes-operator/commit/5dfadeea58ab1c6fceb07a1eca7c0836ecb62ea8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump croniter from 3.0.4 to 5.0.1
  ([#448](https://github.com/Twingate/kubernetes-operator/pull/448),
  [`1e1c26b`](https://github.com/Twingate/kubernetes-operator/commit/1e1c26b5bdcaf3083cf3e4453842f64637436d9f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump factory-boy from 3.3.0 to 3.3.1
  ([#387](https://github.com/Twingate/kubernetes-operator/pull/387),
  [`5dfdd7e`](https://github.com/Twingate/kubernetes-operator/commit/5dfdd7ed2cb4be6910c88416873d58fde4fc730e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump github.com/gruntwork-io/terratest from 0.46.16 to 0.47.0
  ([#353](https://github.com/Twingate/kubernetes-operator/pull/353),
  [`1becc60`](https://github.com/Twingate/kubernetes-operator/commit/1becc605fd89d48b8a5cbdd533b46124864009fd))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump github.com/gruntwork-io/terratest from 0.47.0 to 0.47.1
  ([#393](https://github.com/Twingate/kubernetes-operator/pull/393),
  [`7038f3a`](https://github.com/Twingate/kubernetes-operator/commit/7038f3afa48a87a2e046a6b4b25ac59b9243d236))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump github.com/gruntwork-io/terratest from 0.47.1 to 0.47.2
  ([#419](https://github.com/Twingate/kubernetes-operator/pull/419),
  [`e218644`](https://github.com/Twingate/kubernetes-operator/commit/e218644f7db742080f497424db5ac346db015578))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google-cloud-artifact-registry from 1.11.3 to 1.11.4
  ([#351](https://github.com/Twingate/kubernetes-operator/pull/351),
  [`d1d14ad`](https://github.com/Twingate/kubernetes-operator/commit/d1d14ad667853adb89fc962deceb17bb95e328f4))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google-cloud-artifact-registry from 1.11.4 to 1.11.5
  ([#380](https://github.com/Twingate/kubernetes-operator/pull/380),
  [`86014ce`](https://github.com/Twingate/kubernetes-operator/commit/86014ce5b11d789295fb6cd3bd9cc515280e789b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google-cloud-artifact-registry from 1.11.5 to 1.12.0
  ([#441](https://github.com/Twingate/kubernetes-operator/pull/441),
  [`7afc39f`](https://github.com/Twingate/kubernetes-operator/commit/7afc39f7d2be456ef71040a1a747094104ea4b78))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google-cloud-artifact-registry from 1.12.0 to 1.13.0
  ([#447](https://github.com/Twingate/kubernetes-operator/pull/447),
  [`89678be`](https://github.com/Twingate/kubernetes-operator/commit/89678bea9d9ce0790c8135882bec19e7c9000685))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump kubernetes from 30.1.0 to 31.0.0
  ([#409](https://github.com/Twingate/kubernetes-operator/pull/409),
  [`f6d0500`](https://github.com/Twingate/kubernetes-operator/commit/f6d0500284ec9a2ce9183e31b898fdd70246cf3f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump mypy from 1.10.1 to 1.11.0 ([#361](https://github.com/Twingate/kubernetes-operator/pull/361),
  [`aa27f17`](https://github.com/Twingate/kubernetes-operator/commit/aa27f1782f33746ccd7fdd0ca7b0d33a5772d3a3))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump mypy from 1.11.0 to 1.11.1 ([#379](https://github.com/Twingate/kubernetes-operator/pull/379),
  [`3b4587f`](https://github.com/Twingate/kubernetes-operator/commit/3b4587fe2a66f2e31be7afbf44ad7a0bb5b4d36a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump mypy from 1.11.1 to 1.11.2 ([#392](https://github.com/Twingate/kubernetes-operator/pull/392),
  [`7a27253`](https://github.com/Twingate/kubernetes-operator/commit/7a27253a7b70bf9204399497f59736d677c37063))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump mypy from 1.11.2 to 1.12.0 ([#428](https://github.com/Twingate/kubernetes-operator/pull/428),
  [`fd0e177`](https://github.com/Twingate/kubernetes-operator/commit/fd0e17701618f0695ffca9fc6098a38a3d547a0a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump mypy from 1.12.0 to 1.12.1 ([#436](https://github.com/Twingate/kubernetes-operator/pull/436),
  [`9040578`](https://github.com/Twingate/kubernetes-operator/commit/90405786bc27ff26f4a7f745f4f4885df7f7c8c7))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump mypy from 1.12.1 to 1.13.0 ([#439](https://github.com/Twingate/kubernetes-operator/pull/439),
  [`91d9126`](https://github.com/Twingate/kubernetes-operator/commit/91d9126e7ad1a473183b0be3f71132ed4e37ee3f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.10 to 3.10.11
  ([#451](https://github.com/Twingate/kubernetes-operator/pull/451),
  [`32b353e`](https://github.com/Twingate/kubernetes-operator/commit/32b353eb067e6f424908ca7e773cc71c1fe3b428))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.6 to 3.10.7
  ([#383](https://github.com/Twingate/kubernetes-operator/pull/383),
  [`f44d7dc`](https://github.com/Twingate/kubernetes-operator/commit/f44d7dc4a16454c4e6a63fc3259cc97a8a9eda54))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.7 to 3.10.9
  ([#437](https://github.com/Twingate/kubernetes-operator/pull/437),
  [`8b91596`](https://github.com/Twingate/kubernetes-operator/commit/8b915962974b8abd32c55ab8655e73b7fb3a51d2))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.9 to 3.10.10
  ([#440](https://github.com/Twingate/kubernetes-operator/pull/440),
  [`376dd8a`](https://github.com/Twingate/kubernetes-operator/commit/376dd8ac237fcbabaa08b8d72cac73b2eda979bf))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pre-commit from 3.7.1 to 3.8.0
  ([#376](https://github.com/Twingate/kubernetes-operator/pull/376),
  [`d13be35`](https://github.com/Twingate/kubernetes-operator/commit/d13be351b2a5b5602eb9b22d7571f0064b82effc))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pre-commit from 3.8.0 to 4.0.1
  ([#425](https://github.com/Twingate/kubernetes-operator/pull/425),
  [`7b6ab07`](https://github.com/Twingate/kubernetes-operator/commit/7b6ab076db82ae93b678c7a67ab347b0c56650be))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.8.0 to 2.8.2
  ([#345](https://github.com/Twingate/kubernetes-operator/pull/345),
  [`633d0c3`](https://github.com/Twingate/kubernetes-operator/commit/633d0c3b102d7c4ebd54fdc97ba8671ddb45b0d6))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.8.2 to 2.9.0
  ([#398](https://github.com/Twingate/kubernetes-operator/pull/398),
  [`ee34d0e`](https://github.com/Twingate/kubernetes-operator/commit/ee34d0ef06d7e002c482672590ef8ac39df77de6))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

- Bump pydantic from 2.9.0 to 2.9.1
  ([#401](https://github.com/Twingate/kubernetes-operator/pull/401),
  [`077be19`](https://github.com/Twingate/kubernetes-operator/commit/077be196e6686c352060c0822b810831353573ba))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.9.1 to 2.9.2
  ([#408](https://github.com/Twingate/kubernetes-operator/pull/408),
  [`04b6514`](https://github.com/Twingate/kubernetes-operator/commit/04b65140b9eb1cd5a58330fb9f046e05fc33ae2d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.3.4 to 2.4.0
  ([#377](https://github.com/Twingate/kubernetes-operator/pull/377),
  [`b19e5b5`](https://github.com/Twingate/kubernetes-operator/commit/b19e5b5c0b044d76e7ec92245d7012ee76ee5b85))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.4.0 to 2.5.2
  ([#405](https://github.com/Twingate/kubernetes-operator/pull/405),
  [`1bbcbe0`](https://github.com/Twingate/kubernetes-operator/commit/1bbcbe01169c8b3b9fe38e4b43070fadb154b582))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.5.2 to 2.6.0
  ([#433](https://github.com/Twingate/kubernetes-operator/pull/433),
  [`c51fce3`](https://github.com/Twingate/kubernetes-operator/commit/c51fce3d7a76cbf25c67a395d6a4339626b9a1f9))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.6.0 to 2.6.1
  ([#450](https://github.com/Twingate/kubernetes-operator/pull/450),
  [`b42d9f5`](https://github.com/Twingate/kubernetes-operator/commit/b42d9f5d9bdbc64315e3d272750a450aac639f11))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 8.2.2 to 8.3.1 ([#359](https://github.com/Twingate/kubernetes-operator/pull/359),
  [`1abcfd8`](https://github.com/Twingate/kubernetes-operator/commit/1abcfd82392f5f62b07b847c3cb76826a1066d58))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 8.3.1 to 8.3.2 ([#369](https://github.com/Twingate/kubernetes-operator/pull/369),
  [`0e3c380`](https://github.com/Twingate/kubernetes-operator/commit/0e3c3801c272bb927229bb0938e5d8f0c52f0b8a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 8.3.2 to 8.3.3 ([#404](https://github.com/Twingate/kubernetes-operator/pull/404),
  [`cb46953`](https://github.com/Twingate/kubernetes-operator/commit/cb469536636728777d87616397bc64774a5a8618))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest-randomly from 3.15.0 to 3.16.0
  ([#445](https://github.com/Twingate/kubernetes-operator/pull/445),
  [`1de3f80`](https://github.com/Twingate/kubernetes-operator/commit/1de3f809d866282baf1899a3de64abd94ccef1ee))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.10.0 to 9.10.1
  ([#426](https://github.com/Twingate/kubernetes-operator/pull/426),
  [`53bf3bb`](https://github.com/Twingate/kubernetes-operator/commit/53bf3bb34fdcf0e24e6358620a4621143eaf12c8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.10.1 to 9.11.0
  ([#429](https://github.com/Twingate/kubernetes-operator/pull/429),
  [`f85f585`](https://github.com/Twingate/kubernetes-operator/commit/f85f585223e11213df6b4a84bd995351d8593dde))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.11.0 to 9.11.1
  ([#431](https://github.com/Twingate/kubernetes-operator/pull/431),
  [`4d841d5`](https://github.com/Twingate/kubernetes-operator/commit/4d841d53cfaf420677efd9ba587e4de42a0890ca))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.11.1 to 9.12.0
  ([#434](https://github.com/Twingate/kubernetes-operator/pull/434),
  [`fda0a57`](https://github.com/Twingate/kubernetes-operator/commit/fda0a57153d196c64f0e41c0cbcb5ffa95b5a4b8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.8.3 to 9.8.4
  ([#346](https://github.com/Twingate/kubernetes-operator/pull/346),
  [`db13a96`](https://github.com/Twingate/kubernetes-operator/commit/db13a9660e449110b6c31d835a29c8f84f65d2b0))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.8.4 to 9.8.5
  ([#350](https://github.com/Twingate/kubernetes-operator/pull/350),
  [`629260a`](https://github.com/Twingate/kubernetes-operator/commit/629260a7fbc5e0438dc4112d6849be5d77b2f29a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.8.5 to 9.8.6
  ([#363](https://github.com/Twingate/kubernetes-operator/pull/363),
  [`5d99d5d`](https://github.com/Twingate/kubernetes-operator/commit/5d99d5dced95a1ae4126460927353403f63e6f36))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.8.6 to 9.8.7
  ([#388](https://github.com/Twingate/kubernetes-operator/pull/388),
  [`ec6f1fd`](https://github.com/Twingate/kubernetes-operator/commit/ec6f1fd7e09aeb2a92120510bb2909ce29e1b77d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.8.7 to 9.8.8
  ([#395](https://github.com/Twingate/kubernetes-operator/pull/395),
  [`e36c1de`](https://github.com/Twingate/kubernetes-operator/commit/e36c1de4272a3cbde6dc4fb259e309cce0666727))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.8.8 to 9.8.9
  ([#417](https://github.com/Twingate/kubernetes-operator/pull/417),
  [`e41a483`](https://github.com/Twingate/kubernetes-operator/commit/e41a483a94033fc0a6402f16443e55f45b4e7d90))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.8.9 to 9.9.0
  ([#418](https://github.com/Twingate/kubernetes-operator/pull/418),
  [`0eac57c`](https://github.com/Twingate/kubernetes-operator/commit/0eac57c57a01d7b1afa57aaddd97a6d8cc49526c))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.9.0 to 9.10.0
  ([#424](https://github.com/Twingate/kubernetes-operator/pull/424),
  [`c3808e2`](https://github.com/Twingate/kubernetes-operator/commit/c3808e27279d706f6860c58a401e7e5317f221c5))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pyupgrade from 3.16.0 to 3.17.0
  ([#374](https://github.com/Twingate/kubernetes-operator/pull/374),
  [`0eed8c8`](https://github.com/Twingate/kubernetes-operator/commit/0eed8c81bc2c9f230e29979d3e6c639602c3ac26))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pyupgrade from 3.17.0 to 3.18.0
  ([#430](https://github.com/Twingate/kubernetes-operator/pull/430),
  [`f716a95`](https://github.com/Twingate/kubernetes-operator/commit/f716a95649826a2ba18e2746163aa4a176ec5e5c))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pyupgrade from 3.18.0 to 3.19.0
  ([#438](https://github.com/Twingate/kubernetes-operator/pull/438),
  [`5b12b4e`](https://github.com/Twingate/kubernetes-operator/commit/5b12b4eaf60691eacfd7b3c220026bdd90cdfae5))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.5.0 to 0.5.1 ([#349](https://github.com/Twingate/kubernetes-operator/pull/349),
  [`357a4d6`](https://github.com/Twingate/kubernetes-operator/commit/357a4d67269be50a43c4f57f87d3ab8c684d45ac))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.5.1 to 0.5.2 ([#354](https://github.com/Twingate/kubernetes-operator/pull/354),
  [`e7c76ae`](https://github.com/Twingate/kubernetes-operator/commit/e7c76ae13459424d0f98bab59def5b6d93fd59a2))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.5.2 to 0.5.3 ([#358](https://github.com/Twingate/kubernetes-operator/pull/358),
  [`d7ef48a`](https://github.com/Twingate/kubernetes-operator/commit/d7ef48aa0d4b9b38efc6351758c6afc6ca27bd10))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.5.3 to 0.5.4 ([#360](https://github.com/Twingate/kubernetes-operator/pull/360),
  [`15c6827`](https://github.com/Twingate/kubernetes-operator/commit/15c68276cc9dc669854ce715de012f64733c3414))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.5.4 to 0.5.5 ([#372](https://github.com/Twingate/kubernetes-operator/pull/372),
  [`b48ce95`](https://github.com/Twingate/kubernetes-operator/commit/b48ce95f46e7143e743932f1809c821a16ead024))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.5.5 to 0.5.6 ([#381](https://github.com/Twingate/kubernetes-operator/pull/381),
  [`4c4cd41`](https://github.com/Twingate/kubernetes-operator/commit/4c4cd41531c1a65bb3009f00e904ad9f554964f8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.5.6 to 0.5.7 ([#382](https://github.com/Twingate/kubernetes-operator/pull/382),
  [`0c1fc84`](https://github.com/Twingate/kubernetes-operator/commit/0c1fc844206d844467aa44cf78afb4673c3ea850))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.5.7 to 0.6.2 ([#391](https://github.com/Twingate/kubernetes-operator/pull/391),
  [`0c26ca3`](https://github.com/Twingate/kubernetes-operator/commit/0c26ca3ccc25500ad59019eea5d39312e85ffe7c))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

- Bump ruff from 0.6.2 to 0.6.3 ([#394](https://github.com/Twingate/kubernetes-operator/pull/394),
  [`373aa1f`](https://github.com/Twingate/kubernetes-operator/commit/373aa1fe671ca0ced889702498aed752622a384d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.6.3 to 0.6.4 ([#399](https://github.com/Twingate/kubernetes-operator/pull/399),
  [`de387fd`](https://github.com/Twingate/kubernetes-operator/commit/de387fd30cc4561b132363f60fc4d9cc37ab640a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.6.4 to 0.6.5 ([#406](https://github.com/Twingate/kubernetes-operator/pull/406),
  [`89e9efe`](https://github.com/Twingate/kubernetes-operator/commit/89e9efed571958b743621268af202ed2a295e134))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.6.5 to 0.6.6 ([#410](https://github.com/Twingate/kubernetes-operator/pull/410),
  [`bf3f798`](https://github.com/Twingate/kubernetes-operator/commit/bf3f798137c1f6f9b86c5cbe7cb078e3896c7406))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.6.6 to 0.6.7 ([#411](https://github.com/Twingate/kubernetes-operator/pull/411),
  [`61ab430`](https://github.com/Twingate/kubernetes-operator/commit/61ab430eb97f2b69a65b31ef3da0672f6e18f5fd))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.6.7 to 0.6.8 ([#416](https://github.com/Twingate/kubernetes-operator/pull/416),
  [`fa8c761`](https://github.com/Twingate/kubernetes-operator/commit/fa8c7619605e13115831673a621fbcaa8c7ee7be))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <205185+ekampf@users.noreply.github.com>

- Bump ruff from 0.6.8 to 0.6.9 ([#422](https://github.com/Twingate/kubernetes-operator/pull/422),
  [`0dd8063`](https://github.com/Twingate/kubernetes-operator/commit/0dd80630f2adcc7ae754d327aea282f4cf81d622))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.6.9 to 0.7.0 ([#435](https://github.com/Twingate/kubernetes-operator/pull/435),
  [`fcc1ffe`](https://github.com/Twingate/kubernetes-operator/commit/fcc1ffe09175ce5901e018acf60110b10f559597))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.7.0 to 0.7.1 ([#443](https://github.com/Twingate/kubernetes-operator/pull/443),
  [`f429127`](https://github.com/Twingate/kubernetes-operator/commit/f4291270d879860d8688704640e49219cc52535a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.7.1 to 0.7.2 ([#452](https://github.com/Twingate/kubernetes-operator/pull/452),
  [`08995b7`](https://github.com/Twingate/kubernetes-operator/commit/08995b71b80cddd22a2c1ecf89575bdd9e23a985))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump setuptools from 68.2.0 to 70.0.0
  ([#355](https://github.com/Twingate/kubernetes-operator/pull/355),
  [`69664ac`](https://github.com/Twingate/kubernetes-operator/commit/69664acb92ec6df2ba2b3147277aa842397f5670))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump syrupy from 4.6.1 to 4.6.4 ([#389](https://github.com/Twingate/kubernetes-operator/pull/389),
  [`71209d7`](https://github.com/Twingate/kubernetes-operator/commit/71209d73e99419bca13afaab94239fa2a6d38025))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump syrupy from 4.6.4 to 4.7.1 ([#390](https://github.com/Twingate/kubernetes-operator/pull/390),
  [`84c794a`](https://github.com/Twingate/kubernetes-operator/commit/84c794a73bb090b2b5811a01f28e253b00440ca0))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump syrupy from 4.7.1 to 4.7.2 ([#423](https://github.com/Twingate/kubernetes-operator/pull/423),
  [`9cdf0bb`](https://github.com/Twingate/kubernetes-operator/commit/9cdf0bb84716d4892e27a27f8a1c5f479760dfc0))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump tenacity from 8.4.2 to 8.5.0
  ([#347](https://github.com/Twingate/kubernetes-operator/pull/347),
  [`c73fa81`](https://github.com/Twingate/kubernetes-operator/commit/c73fa817b722460a129eaadc28f6d5735023c9bb))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump tenacity from 8.5.0 to 9.0.0
  ([#373](https://github.com/Twingate/kubernetes-operator/pull/373),
  [`4fbc93a`](https://github.com/Twingate/kubernetes-operator/commit/4fbc93a8909592aaeb11542d1c27ec815a9c2cc6))

- Bump types-croniter from 2.0.0.20240423 to 2.0.5.20240717
  ([#356](https://github.com/Twingate/kubernetes-operator/pull/356),
  [`627834f`](https://github.com/Twingate/kubernetes-operator/commit/627834ff5dbe0487c37ba18688b3fb7d09b90d19))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-croniter from 2.0.5.20240717 to 2.0.5.20240722
  ([#362](https://github.com/Twingate/kubernetes-operator/pull/362),
  [`865295c`](https://github.com/Twingate/kubernetes-operator/commit/865295cc5fc38102dcafcfe268c0a199d3c3f983))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-croniter from 2.0.5.20240722 to 3.0.3.20240731
  ([#378](https://github.com/Twingate/kubernetes-operator/pull/378),
  [`60d6f18`](https://github.com/Twingate/kubernetes-operator/commit/60d6f18cd4b5b15722407daff2e22e1ecc429bda))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-croniter from 3.0.3.20240731 to 3.0.4.20241027
  ([#444](https://github.com/Twingate/kubernetes-operator/pull/444),
  [`c5c35ec`](https://github.com/Twingate/kubernetes-operator/commit/c5c35eccb27ab5b53adc03d40f769a143dbeece9))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-croniter from 3.0.4.20241027 to 4.0.0.20241030
  ([#449](https://github.com/Twingate/kubernetes-operator/pull/449),
  [`d9812fa`](https://github.com/Twingate/kubernetes-operator/commit/d9812fa064a89f8f7f423f0ec6ef7aa181aee927))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.32.0.20240622 to 2.32.0.20240712
  ([#352](https://github.com/Twingate/kubernetes-operator/pull/352),
  [`62a0dcc`](https://github.com/Twingate/kubernetes-operator/commit/62a0dcc4bd46028ffb1c35410565312db5b6ca1a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.32.0.20240712 to 2.32.0.20240905
  ([#396](https://github.com/Twingate/kubernetes-operator/pull/396),
  [`7118358`](https://github.com/Twingate/kubernetes-operator/commit/7118358fe59b141d85dc0525e9f3ef1603a2ee7b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.32.0.20240905 to 2.32.0.20240907
  ([#402](https://github.com/Twingate/kubernetes-operator/pull/402),
  [`8adb4ee`](https://github.com/Twingate/kubernetes-operator/commit/8adb4ee67a8d31650ce498f0f36c4d760d9f6934))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.32.0.20240907 to 2.32.0.20240914
  ([#407](https://github.com/Twingate/kubernetes-operator/pull/407),
  [`420449c`](https://github.com/Twingate/kubernetes-operator/commit/420449c03c0412003f0a64c021a759c48c837848))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.32.0.20240914 to 2.32.0.20241016
  ([#432](https://github.com/Twingate/kubernetes-operator/pull/432),
  [`c31c74c`](https://github.com/Twingate/kubernetes-operator/commit/c31c74cc6b122780ec3cb34d8ff04f91faf86f9f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Re-enable poetry package mode setting to be False
  ([`7473698`](https://github.com/Twingate/kubernetes-operator/commit/74736982fde898144aac51f4e3fd15da603c9e6d))

### Features

- Nicer `kubectl get` for TwingateResource and TwingateConnector
  ([#366](https://github.com/Twingate/kubernetes-operator/pull/366),
  [`7f5697f`](https://github.com/Twingate/kubernetes-operator/commit/7f5697f3ae37b6cc1ad0a26815794d4096a7f6f8))

- Support referencing TwingateGroup from TwingateResourceAccess
  ([#412](https://github.com/Twingate/kubernetes-operator/pull/412),
  [`c27f98f`](https://github.com/Twingate/kubernetes-operator/commit/c27f98f02dabd353d2bf55d0d5f9ae803c58ec0b))

- Twingategroup object - support creating groups via k8s object
  ([#397](https://github.com/Twingate/kubernetes-operator/pull/397),
  [`3a1c530`](https://github.com/Twingate/kubernetes-operator/commit/3a1c5303c5d23d414406e30617ce616fa502b5c1))

### Testing

- Improve integration tests stability
  ([#415](https://github.com/Twingate/kubernetes-operator/pull/415),
  [`95562f3`](https://github.com/Twingate/kubernetes-operator/commit/95562f3a94acd5329857b1d08dd814cc8de0ac4b))

- More tests for TwingateGroup Handlers
  ([#413](https://github.com/Twingate/kubernetes-operator/pull/413),
  [`2132cfa`](https://github.com/Twingate/kubernetes-operator/commit/2132cfa970362c1c9652dc5640efbdf5c2370dbf))

- Re-enable test_resource_access_flows tests
  ([`1ff633f`](https://github.com/Twingate/kubernetes-operator/commit/1ff633f3dfd38e60fc581b4ed17d5565e390ebb6))


## v0.11.5 (2024-07-03)

### Chores

- Bump github.com/gruntwork-io/terratest from 0.46.15 to 0.46.16
  ([#339](https://github.com/Twingate/kubernetes-operator/pull/339),
  [`d58d845`](https://github.com/Twingate/kubernetes-operator/commit/d58d845bbb8c2616e0ad18f621de1efa38c4d727))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump mypy from 1.10.0 to 1.10.1 ([#335](https://github.com/Twingate/kubernetes-operator/pull/335),
  [`2bf326a`](https://github.com/Twingate/kubernetes-operator/commit/2bf326ad4458cf11bb130301d636aa3ed0da9514))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.5 to 3.10.6
  ([#342](https://github.com/Twingate/kubernetes-operator/pull/342),
  [`f7c24bd`](https://github.com/Twingate/kubernetes-operator/commit/f7c24bd77b4399c2e41868ce6de0f39aeec34f10))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.7.4 to 2.8.0
  ([#341](https://github.com/Twingate/kubernetes-operator/pull/341),
  [`db3d023`](https://github.com/Twingate/kubernetes-operator/commit/db3d0235118fd08d615220d24ab49bbcbcc92b98))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.3.3 to 2.3.4
  ([#334](https://github.com/Twingate/kubernetes-operator/pull/334),
  [`93f0747`](https://github.com/Twingate/kubernetes-operator/commit/93f0747c513f29bd7fe6efa50cfb4109f05d45f8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.4.10 to 0.5.0 ([#340](https://github.com/Twingate/kubernetes-operator/pull/340),
  [`353060a`](https://github.com/Twingate/kubernetes-operator/commit/353060a6542768a70b6290d877ebc46bb5950465))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

- Bump tenacity from 8.4.1 to 8.4.2
  ([#336](https://github.com/Twingate/kubernetes-operator/pull/336),
  [`3b91830`](https://github.com/Twingate/kubernetes-operator/commit/3b9183015f6fe73f93fbdbbddf582ea9880b2ec4))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>


## v0.11.4 (2024-06-24)

### Bug Fixes

- Allow connectors to run under Restricted pod-security policy
  ([#329](https://github.com/Twingate/kubernetes-operator/pull/329),
  [`14302df`](https://github.com/Twingate/kubernetes-operator/commit/14302df61105d8ce4d4423d03626008c1df7e8b1))

### Chores

- Bump bandit from 1.7.8 to 1.7.9 ([#321](https://github.com/Twingate/kubernetes-operator/pull/321),
  [`64523df`](https://github.com/Twingate/kubernetes-operator/commit/64523df8b1f60e2cafee6202744bb651c73de492))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump danger/danger-js from 12.2.0 to 12.3.0
  ([#295](https://github.com/Twingate/kubernetes-operator/pull/295),
  [`a752166`](https://github.com/Twingate/kubernetes-operator/commit/a752166824394c90e321b748933228e8473f4ccc))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump danger/danger-js from 12.3.0 to 12.3.1
  ([#311](https://github.com/Twingate/kubernetes-operator/pull/311),
  [`9309f19`](https://github.com/Twingate/kubernetes-operator/commit/9309f1989c71bcbccf09af2d249e9c9ea078903b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump danger/danger-js from 12.3.1 to 12.3.3
  ([#331](https://github.com/Twingate/kubernetes-operator/pull/331),
  [`ff0a8e1`](https://github.com/Twingate/kubernetes-operator/commit/ff0a8e14f86a49374987c1404dcda66c404426c0))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump github.com/gruntwork-io/terratest from 0.46.14 to 0.46.15
  ([#297](https://github.com/Twingate/kubernetes-operator/pull/297),
  [`9142339`](https://github.com/Twingate/kubernetes-operator/commit/9142339f39abb350d06253a704cefa9ae493fc82))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump kubernetes from 29.0.0 to 30.1.0
  ([#314](https://github.com/Twingate/kubernetes-operator/pull/314),
  [`b5fccd0`](https://github.com/Twingate/kubernetes-operator/commit/b5fccd0f68de5e57b075f6da8f31a506dd9c3592))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.3 to 3.10.4
  ([#317](https://github.com/Twingate/kubernetes-operator/pull/317),
  [`2c9f2e7`](https://github.com/Twingate/kubernetes-operator/commit/2c9f2e7fa07ac5811ebd950a389605602dbddc86))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.4 to 3.10.5
  ([#322](https://github.com/Twingate/kubernetes-operator/pull/322),
  [`1c0a0ea`](https://github.com/Twingate/kubernetes-operator/commit/1c0a0ea711d840e4f5acf961b6aa269cd88d180c))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.7.1 to 2.7.2
  ([#303](https://github.com/Twingate/kubernetes-operator/pull/303),
  [`c5d4648`](https://github.com/Twingate/kubernetes-operator/commit/c5d46486eeda8d63ddd3eade8c765da8aa9e24b7))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.7.2 to 2.7.3
  ([#308](https://github.com/Twingate/kubernetes-operator/pull/308),
  [`9569663`](https://github.com/Twingate/kubernetes-operator/commit/9569663df45cfe6fb0553c78ae2e81fa0f1c593e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.7.3 to 2.7.4
  ([#319](https://github.com/Twingate/kubernetes-operator/pull/319),
  [`e88c317`](https://github.com/Twingate/kubernetes-operator/commit/e88c317afbfe4a0216c55dafa558b7c65da20d0f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.2.1 to 2.3.0
  ([#307](https://github.com/Twingate/kubernetes-operator/pull/307),
  [`a4eb52e`](https://github.com/Twingate/kubernetes-operator/commit/a4eb52e6d7388627ff84047cfecf106db22f4322))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.3.0 to 2.3.1
  ([#313](https://github.com/Twingate/kubernetes-operator/pull/313),
  [`c172a45`](https://github.com/Twingate/kubernetes-operator/commit/c172a45983ba1fce6aecf7f7813652a9b25eaced))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.3.1 to 2.3.2
  ([#318](https://github.com/Twingate/kubernetes-operator/pull/318),
  [`2733fb5`](https://github.com/Twingate/kubernetes-operator/commit/2733fb52192ac9eca8d558f8a8f82f325b9c3590))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.3.2 to 2.3.3
  ([#320](https://github.com/Twingate/kubernetes-operator/pull/320),
  [`3dcfe30`](https://github.com/Twingate/kubernetes-operator/commit/3dcfe30c9345fb397b1e68c4c064bc5c3782e30d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 8.2.1 to 8.2.2 ([#310](https://github.com/Twingate/kubernetes-operator/pull/310),
  [`48a2b78`](https://github.com/Twingate/kubernetes-operator/commit/48a2b7888eae2fd55c286725928563ef7177f890))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.7.3 to 9.8.0
  ([#301](https://github.com/Twingate/kubernetes-operator/pull/301),
  [`7c2ebec`](https://github.com/Twingate/kubernetes-operator/commit/7c2ebecce3ecf6160245c955aa47251a23181ca9))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.8.0 to 9.8.1
  ([#309](https://github.com/Twingate/kubernetes-operator/pull/309),
  [`56d33da`](https://github.com/Twingate/kubernetes-operator/commit/56d33dacd98ac01d59d5999c6f274103cbd2be85))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.8.1 to 9.8.2
  ([#325](https://github.com/Twingate/kubernetes-operator/pull/325),
  [`204df1b`](https://github.com/Twingate/kubernetes-operator/commit/204df1bd4eb1c2fd5d4598af8f85df04888770ac))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.8.2 to 9.8.3
  ([#328](https://github.com/Twingate/kubernetes-operator/pull/328),
  [`af0a52f`](https://github.com/Twingate/kubernetes-operator/commit/af0a52f40f562f325b97c83199d27362403cb82e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pyupgrade from 3.15.2 to 3.16.0
  ([#316](https://github.com/Twingate/kubernetes-operator/pull/316),
  [`201d69a`](https://github.com/Twingate/kubernetes-operator/commit/201d69a0fb2ac2244c422f3a4699e7b0894d6946))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump requests from 2.31.0 to 2.32.1
  ([#294](https://github.com/Twingate/kubernetes-operator/pull/294),
  [`7935746`](https://github.com/Twingate/kubernetes-operator/commit/7935746bd45f867cefe78d77abed472fbda948b4))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump requests from 2.32.1 to 2.32.2
  ([#296](https://github.com/Twingate/kubernetes-operator/pull/296),
  [`18038ea`](https://github.com/Twingate/kubernetes-operator/commit/18038ea6936a08a511fa15363879b378b9fa3dc7))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump requests from 2.32.2 to 2.32.3
  ([#304](https://github.com/Twingate/kubernetes-operator/pull/304),
  [`2aa20be`](https://github.com/Twingate/kubernetes-operator/commit/2aa20be75fe6e93e37425d6d4ccaeb8de9813f4d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump responses from 0.25.0 to 0.25.2
  ([#315](https://github.com/Twingate/kubernetes-operator/pull/315),
  [`be5ff6e`](https://github.com/Twingate/kubernetes-operator/commit/be5ff6e28cf562cc29ee650ada7fdeb0c53d9204))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump responses from 0.25.2 to 0.25.3
  ([#324](https://github.com/Twingate/kubernetes-operator/pull/324),
  [`7f636e4`](https://github.com/Twingate/kubernetes-operator/commit/7f636e4f333fffacaff0d37dbe08da4c6d90258a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.4.4 to 0.4.5 ([#298](https://github.com/Twingate/kubernetes-operator/pull/298),
  [`ad48803`](https://github.com/Twingate/kubernetes-operator/commit/ad48803f51b18d451f340dd9f522fc227b204a9c))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.4.5 to 0.4.6 ([#302](https://github.com/Twingate/kubernetes-operator/pull/302),
  [`317a197`](https://github.com/Twingate/kubernetes-operator/commit/317a197bf9dbffdd86ec8b76024de7893674186c))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.4.6 to 0.4.7 ([#306](https://github.com/Twingate/kubernetes-operator/pull/306),
  [`b04e7ee`](https://github.com/Twingate/kubernetes-operator/commit/b04e7ee8d8dd98710ddc5d29d3257a066f2199c6))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.4.7 to 0.4.8 ([#312](https://github.com/Twingate/kubernetes-operator/pull/312),
  [`ab409ac`](https://github.com/Twingate/kubernetes-operator/commit/ab409acebd453f9afd066eb81784943c8daf410f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.4.8 to 0.4.9 ([#323](https://github.com/Twingate/kubernetes-operator/pull/323),
  [`fa36571`](https://github.com/Twingate/kubernetes-operator/commit/fa3657197dc552d28a9e8088c0452effc1326fd6))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.4.9 to 0.4.10 ([#332](https://github.com/Twingate/kubernetes-operator/pull/332),
  [`0584245`](https://github.com/Twingate/kubernetes-operator/commit/0584245905f92f44fc328fb2cbe48991091f4a03))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump tenacity from 8.3.0 to 8.4.1
  ([#326](https://github.com/Twingate/kubernetes-operator/pull/326),
  [`54ccc57`](https://github.com/Twingate/kubernetes-operator/commit/54ccc574545f073a8f3d700247e00de1aeb91994))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.31.0.20240406 to 2.32.0.20240521
  ([#293](https://github.com/Twingate/kubernetes-operator/pull/293),
  [`1751140`](https://github.com/Twingate/kubernetes-operator/commit/1751140d8d8060957ccdaec30f7441d9c9ff6048))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.32.0.20240521 to 2.32.0.20240523
  ([#299](https://github.com/Twingate/kubernetes-operator/pull/299),
  [`f4d7c25`](https://github.com/Twingate/kubernetes-operator/commit/f4d7c259d820e25058f1ade43fe548c548f9bae0))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.32.0.20240523 to 2.32.0.20240602
  ([#305](https://github.com/Twingate/kubernetes-operator/pull/305),
  [`b965d94`](https://github.com/Twingate/kubernetes-operator/commit/b965d940b7b938d0da352dcae326551358b4ee5a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.32.0.20240602 to 2.32.0.20240622
  ([#333](https://github.com/Twingate/kubernetes-operator/pull/333),
  [`bda3eca`](https://github.com/Twingate/kubernetes-operator/commit/bda3ecab987090e6ad6fa625b01e603dd24e3bfd))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump urllib3 from 2.1.0 to 2.2.2
  ([#327](https://github.com/Twingate/kubernetes-operator/pull/327),
  [`7632e25`](https://github.com/Twingate/kubernetes-operator/commit/7632e25d86ef097b972561feb1266603f152d7ea))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- More stable integration tests
  ([`be6da04`](https://github.com/Twingate/kubernetes-operator/commit/be6da046b5b101e9640211e2008227f2c47a268d))


## v0.11.3 (2024-05-20)

### Bug Fixes

- Remove TwingateResourceAccess ownerReference
  ([#289](https://github.com/Twingate/kubernetes-operator/pull/289),
  [`acf0a72`](https://github.com/Twingate/kubernetes-operator/commit/acf0a721853fe5523b0f6f21da79230214325b55))

### Chores

- Bump pytest from 8.2.0 to 8.2.1 ([#291](https://github.com/Twingate/kubernetes-operator/pull/291),
  [`3ce8e82`](https://github.com/Twingate/kubernetes-operator/commit/3ce8e826834fee93a5742166cef7faa31ac29662))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.7.1 to 9.7.2
  ([#284](https://github.com/Twingate/kubernetes-operator/pull/284),
  [`defa346`](https://github.com/Twingate/kubernetes-operator/commit/defa3465ea6d439244a3366063d6fdc525dc1828))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.7.2 to 9.7.3
  ([#288](https://github.com/Twingate/kubernetes-operator/pull/288),
  [`2f856a6`](https://github.com/Twingate/kubernetes-operator/commit/2f856a658e72247177c607529acd4d3d0e14b3cc))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Increase test coverage ([#285](https://github.com/Twingate/kubernetes-operator/pull/285),
  [`28b69f5`](https://github.com/Twingate/kubernetes-operator/commit/28b69f52ce812c43721383397497ac4616f41faa))


## v0.11.2 (2024-05-12)

### Bug Fixes

- Twingateresourceaccess only updating every 10h and not immediately
  ([#283](https://github.com/Twingate/kubernetes-operator/pull/283),
  [`2809bb9`](https://github.com/Twingate/kubernetes-operator/commit/2809bb99417370d767077ed082848038abd03273))

### Chores

- Bump pre-commit from 3.7.0 to 3.7.1
  ([#282](https://github.com/Twingate/kubernetes-operator/pull/282),
  [`2957dd5`](https://github.com/Twingate/kubernetes-operator/commit/2957dd5a402d82ab6dac5ff2bf09219f2464145a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.4.3 to 0.4.4 ([#280](https://github.com/Twingate/kubernetes-operator/pull/280),
  [`261998c`](https://github.com/Twingate/kubernetes-operator/commit/261998c4b84615418d707672a58a8cf65ccfde8d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>


## v0.11.1 (2024-05-08)

### Bug Fixes

- Twingateresourceaccess timer too frequent
  ([`c1645f4`](https://github.com/Twingate/kubernetes-operator/commit/c1645f4a9a5aa43e26ac7ecbe0a2f0a6d0743bc8))


## v0.11.0 (2024-05-07)

### Chores

- Bump danger/danger-js from 12.1.0 to 12.2.0
  ([#272](https://github.com/Twingate/kubernetes-operator/pull/272),
  [`a5b573a`](https://github.com/Twingate/kubernetes-operator/commit/a5b573a8d143b58675743c0406c676467ca36bb8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump jinja2 from 3.1.3 to 3.1.4 ([#276](https://github.com/Twingate/kubernetes-operator/pull/276),
  [`98723bd`](https://github.com/Twingate/kubernetes-operator/commit/98723bd78b61112494b6606c9ff19a8cb094253c))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.2 to 3.10.3
  ([#274](https://github.com/Twingate/kubernetes-operator/pull/274),
  [`98826e4`](https://github.com/Twingate/kubernetes-operator/commit/98826e46127313b78c2595eaea3e18170c5c6a67))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.6.0 to 9.7.0
  ([#273](https://github.com/Twingate/kubernetes-operator/pull/273),
  [`f2f6681`](https://github.com/Twingate/kubernetes-operator/commit/f2f6681f757cf23d46a7176e57c4c485e21f9d30))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.7.0 to 9.7.1
  ([#277](https://github.com/Twingate/kubernetes-operator/pull/277),
  [`ca97d74`](https://github.com/Twingate/kubernetes-operator/commit/ca97d74de284c44b3fe3e5cff2faeb4d4b6a5f9d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.4.2 to 0.4.3 ([#275](https://github.com/Twingate/kubernetes-operator/pull/275),
  [`f05639e`](https://github.com/Twingate/kubernetes-operator/commit/f05639ebb3785f691ea053df579b2272d83cfbf4))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump tenacity from 8.2.3 to 8.3.0
  ([#278](https://github.com/Twingate/kubernetes-operator/pull/278),
  [`f2b8ba9`](https://github.com/Twingate/kubernetes-operator/commit/f2b8ba909daadbe68ccbd6780125d6f228b9fa3c))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Features

- Allow defining custom resource Name for annotated service resource
  ([#279](https://github.com/Twingate/kubernetes-operator/pull/279),
  [`91d3263`](https://github.com/Twingate/kubernetes-operator/commit/91d3263e9de4a1da0e99ea939818e16244d00878))


## v0.10.1 (2024-05-03)

### Bug Fixes

- Using the operator with annotations have some problems
  ([#270](https://github.com/Twingate/kubernetes-operator/pull/270),
  [`ace69fc`](https://github.com/Twingate/kubernetes-operator/commit/ace69fce217626108bf208cc3d69d8080ba9e75a))

### Chores

- Bump mypy from 1.9.0 to 1.10.0 ([#262](https://github.com/Twingate/kubernetes-operator/pull/262),
  [`72e1154`](https://github.com/Twingate/kubernetes-operator/commit/72e1154a19239c0b3fcc1f5712ed324ae8dab161))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.1 to 3.10.2
  ([#268](https://github.com/Twingate/kubernetes-operator/pull/268),
  [`1bf81a3`](https://github.com/Twingate/kubernetes-operator/commit/1bf81a33b5a6a4344e406862caff803772347291))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.7.0 to 2.7.1
  ([#260](https://github.com/Twingate/kubernetes-operator/pull/260),
  [`3f42d4e`](https://github.com/Twingate/kubernetes-operator/commit/3f42d4e1567972919f526a1b86204c804ebb1f04))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 8.1.1 to 8.2.0 ([#266](https://github.com/Twingate/kubernetes-operator/pull/266),
  [`0b591f8`](https://github.com/Twingate/kubernetes-operator/commit/0b591f8dc058016908226af0064ab06dfe721f59))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.4.2 to 9.5.0
  ([#258](https://github.com/Twingate/kubernetes-operator/pull/258),
  [`e5b292d`](https://github.com/Twingate/kubernetes-operator/commit/e5b292d548c7ee347c0ea759b4a3ada35c484c0e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.5.0 to 9.6.0
  ([#267](https://github.com/Twingate/kubernetes-operator/pull/267),
  [`98b925e`](https://github.com/Twingate/kubernetes-operator/commit/98b925e06d2d471e239591f6441625dc362b3cc7))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.4.1 to 0.4.2 ([#263](https://github.com/Twingate/kubernetes-operator/pull/263),
  [`5ddd936`](https://github.com/Twingate/kubernetes-operator/commit/5ddd9369ad55f9506aa69d3a8a5f961ab0d6abd3))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-croniter from 2.0.0.20240321 to 2.0.0.20240423
  ([#259](https://github.com/Twingate/kubernetes-operator/pull/259),
  [`4c42521`](https://github.com/Twingate/kubernetes-operator/commit/4c4252107da145f624b27361746be66ee79a1506))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Update Golang to 1.22.2
  ([`49b9e1f`](https://github.com/Twingate/kubernetes-operator/commit/49b9e1faa591568040ac0f14e16a96f492f204fe))

### Documentation

- Update README
  ([`6516435`](https://github.com/Twingate/kubernetes-operator/commit/65164351a4881d77f7d53b795f1779e22ab2fea4))


## v0.10.0 (2024-04-24)

### Chores

- Bump aiohttp from 3.9.2 to 3.9.4
  ([#254](https://github.com/Twingate/kubernetes-operator/pull/254),
  [`09de547`](https://github.com/Twingate/kubernetes-operator/commit/09de5476be7cb26785b59c751e2b6d4e550d8c48))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump croniter from 2.0.3 to 2.0.5
  ([#257](https://github.com/Twingate/kubernetes-operator/pull/257),
  [`d26366f`](https://github.com/Twingate/kubernetes-operator/commit/d26366f1faeee80939d95d01b10a0ac5b03a3d04))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump danger/danger-js from 11.3.1 to 12.1.0
  ([#253](https://github.com/Twingate/kubernetes-operator/pull/253),
  [`9cd9a8c`](https://github.com/Twingate/kubernetes-operator/commit/9cd9a8c85d3b95115d39586bdb155358eed252cc))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump github.com/gruntwork-io/terratest from 0.46.13 to 0.46.14
  ([#261](https://github.com/Twingate/kubernetes-operator/pull/261),
  [`d346c48`](https://github.com/Twingate/kubernetes-operator/commit/d346c4862be2b42221a5af80fb7a153261281101))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump golang.org/x/net from 0.17.0 to 0.23.0
  ([#255](https://github.com/Twingate/kubernetes-operator/pull/255),
  [`f7cfd19`](https://github.com/Twingate/kubernetes-operator/commit/f7cfd192fc41f7f1ffb6101f94d4293739a0a2e1))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump idna from 3.4 to 3.7 ([#248](https://github.com/Twingate/kubernetes-operator/pull/248),
  [`8fb2baa`](https://github.com/Twingate/kubernetes-operator/commit/8fb2baa7f49400fcc963d63c9cf2e75701862eaf))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.10.0 to 3.10.1
  ([#252](https://github.com/Twingate/kubernetes-operator/pull/252),
  [`f4e8420`](https://github.com/Twingate/kubernetes-operator/commit/f4e84205a27e23753d347538d8f62b6fac6d43bb))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.6.4 to 2.7.0
  ([#250](https://github.com/Twingate/kubernetes-operator/pull/250),
  [`de76253`](https://github.com/Twingate/kubernetes-operator/commit/de7625309afe94c2a0d429986185aaf9222bdb67))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.4.1 to 9.4.2
  ([#251](https://github.com/Twingate/kubernetes-operator/pull/251),
  [`d64708e`](https://github.com/Twingate/kubernetes-operator/commit/d64708e127dd73364d21498737ebd4d71b3c4e23))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.3.5 to 0.3.7 ([#249](https://github.com/Twingate/kubernetes-operator/pull/249),
  [`03542a2`](https://github.com/Twingate/kubernetes-operator/commit/03542a2e8ad1441b64ae5b7eb779e71132859dd8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.3.7 to 0.4.1 ([#256](https://github.com/Twingate/kubernetes-operator/pull/256),
  [`cb2dff2`](https://github.com/Twingate/kubernetes-operator/commit/cb2dff2a0eccdb50c2546a1682bf9d48e65e4f75))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Fix issues stalebot
  ([`92554be`](https://github.com/Twingate/kubernetes-operator/commit/92554beacdecc94f5e7f0fbdff1bec8f36d96c2b))

- Pre-commit updates ([#247](https://github.com/Twingate/kubernetes-operator/pull/247),
  [`aecf20f`](https://github.com/Twingate/kubernetes-operator/commit/aecf20f8f07d96c4c483c29620aa91b9b1581a64))

### Features

- Ability to import existing twingate resources
  ([#246](https://github.com/Twingate/kubernetes-operator/pull/246),
  [`d143995`](https://github.com/Twingate/kubernetes-operator/commit/d143995d46f1a381d0571dfb05df9843d919abcd))

- Allow exposing Service objects with annotations
  ([#244](https://github.com/Twingate/kubernetes-operator/pull/244),
  [`87a8bdc`](https://github.com/Twingate/kubernetes-operator/commit/87a8bdcc51be4b3b87f8e2502a24ae7749d9a5c3))

- Don’t query for principal external ref once we have the id
  ([#243](https://github.com/Twingate/kubernetes-operator/pull/243),
  [`9d6cb8c`](https://github.com/Twingate/kubernetes-operator/commit/9d6cb8ce3eaec241ed1b660df790892b79625189))


## v0.9.0 (2024-04-08)

### Chores

- Bump kopf from 1.37.1 to 1.37.2 ([#240](https://github.com/Twingate/kubernetes-operator/pull/240),
  [`9c43895`](https://github.com/Twingate/kubernetes-operator/commit/9c438959ab2df39f1fdd798738fce50d9a8b21bb))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.4.0 to 9.4.1
  ([#241](https://github.com/Twingate/kubernetes-operator/pull/241),
  [`28ec499`](https://github.com/Twingate/kubernetes-operator/commit/28ec499cf1950b1d29bdca3f0da3e7b205cb40ab))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.31.0.20240403 to 2.31.0.20240406
  ([#242](https://github.com/Twingate/kubernetes-operator/pull/242),
  [`5bc9e9d`](https://github.com/Twingate/kubernetes-operator/commit/5bc9e9d26e992d67643d1bb4d927afba80e53916))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Features

- Add ability to customize kopf logging level
  ([#236](https://github.com/Twingate/kubernetes-operator/pull/236),
  [`1fc2eaf`](https://github.com/Twingate/kubernetes-operator/commit/1fc2eaf5a27cea842ed2dd45bbff726178bbc058))

- Added TwingateConnector `logAnalytics` flag
  ([#237](https://github.com/Twingate/kubernetes-operator/pull/237),
  [`a98acc3`](https://github.com/Twingate/kubernetes-operator/commit/a98acc3f96e7a03d3298e3d94c959ef991f1d821))


## v0.8.0 (2024-04-03)

### Chores

- Add more Ruff linters ([#233](https://github.com/Twingate/kubernetes-operator/pull/233),
  [`7f918be`](https://github.com/Twingate/kubernetes-operator/commit/7f918be0983adad30747bad5c53a561dbf6b25fe))

- Bump orjson from 3.9.15 to 3.10.0
  ([#227](https://github.com/Twingate/kubernetes-operator/pull/227),
  [`6294f36`](https://github.com/Twingate/kubernetes-operator/commit/6294f36869fe7bab751bb353a3e36064170de1e0))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.3.1 to 9.4.0
  ([#229](https://github.com/Twingate/kubernetes-operator/pull/229),
  [`70d6b69`](https://github.com/Twingate/kubernetes-operator/commit/70d6b692de48dbf6030015ff0e31e0d6ea8cfedf))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.3.4 to 0.3.5 ([#230](https://github.com/Twingate/kubernetes-operator/pull/230),
  [`b5075d6`](https://github.com/Twingate/kubernetes-operator/commit/b5075d6dc3194205f1f4c590b34ef19399b55a59))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.31.0.20240311 to 2.31.0.20240402
  ([#231](https://github.com/Twingate/kubernetes-operator/pull/231),
  [`bceef26`](https://github.com/Twingate/kubernetes-operator/commit/bceef261d0d5f2fd99d0bf3e0a92d28166ad0411))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.31.0.20240402 to 2.31.0.20240403
  ([#235](https://github.com/Twingate/kubernetes-operator/pull/235),
  [`72c9c41`](https://github.com/Twingate/kubernetes-operator/commit/72c9c4164dd098e3e7a05ce535b73729e34f6d1a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Features

- Add TwingateConnector sidecarContainers prop
  ([#234](https://github.com/Twingate/kubernetes-operator/pull/234),
  [`835da7c`](https://github.com/Twingate/kubernetes-operator/commit/835da7cc3848c8040096d41938f5d36926ad1618))


## v0.7.0 (2024-03-26)

### Bug Fixes

- Add validation for TwingateConnector when provider is “google”
  ([#224](https://github.com/Twingate/kubernetes-operator/pull/224),
  [`68e188e`](https://github.com/Twingate/kubernetes-operator/commit/68e188ed769822640160a92148a05b0dfbdd41b6))

### Features

- Make TwingateConnector's containerExtra and podExtra mutable
  ([#223](https://github.com/Twingate/kubernetes-operator/pull/223),
  [`e7d8425`](https://github.com/Twingate/kubernetes-operator/commit/e7d84255a64bfd77e5a9f7749471a03cebaeccf6))

- Twingateconnector - allow defining extra pod annotations with `podAnnotations`
  ([#225](https://github.com/Twingate/kubernetes-operator/pull/225),
  [`7b44838`](https://github.com/Twingate/kubernetes-operator/commit/7b44838f8ade8cfcabe79669d32e83a0c31ab9ca))

- Twingateresourceaccess - allow specifying principal by name
  ([#62](https://github.com/Twingate/kubernetes-operator/pull/62),
  [`0b1e69b`](https://github.com/Twingate/kubernetes-operator/commit/0b1e69b14fb2006ff0e30af5d23567b5e718d4f9))


## v0.6.3 (2024-03-25)

### Bug Fixes

- Allow env to be defined in containerExtra
  ([#222](https://github.com/Twingate/kubernetes-operator/pull/222),
  [`14f5ef5`](https://github.com/Twingate/kubernetes-operator/commit/14f5ef5fd14cfee09cd4669ac8b20cb250ee550d))

### Chores

- Bump autoflake from 2.3.0 to 2.3.1
  ([#198](https://github.com/Twingate/kubernetes-operator/pull/198),
  [`edcf38f`](https://github.com/Twingate/kubernetes-operator/commit/edcf38f5592ea4b9163acbb6fd3807015e6f3164))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump bandit from 1.7.7 to 1.7.8 ([#202](https://github.com/Twingate/kubernetes-operator/pull/202),
  [`c7ab9e3`](https://github.com/Twingate/kubernetes-operator/commit/c7ab9e3cc5c41bda1a2649293c0082ceab1f1811))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump croniter from 2.0.2 to 2.0.3
  ([#207](https://github.com/Twingate/kubernetes-operator/pull/207),
  [`9016f41`](https://github.com/Twingate/kubernetes-operator/commit/9016f412913e2f8c0dbc37aadf04a1fe98064469))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump dependabot/fetch-metadata from 1 to 2
  ([#212](https://github.com/Twingate/kubernetes-operator/pull/212),
  [`25bbe4c`](https://github.com/Twingate/kubernetes-operator/commit/25bbe4cffeb16c0d1fbb1d54604b08afa1a1f488))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump github.com/gruntwork-io/terratest from 0.46.12 to 0.46.13
  ([#211](https://github.com/Twingate/kubernetes-operator/pull/211),
  [`d16c8ba`](https://github.com/Twingate/kubernetes-operator/commit/d16c8ba782f95ed84c44a8fc70b398d482001443))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump github.com/gruntwork-io/terratest from 0.46.8 to 0.46.12
  ([#208](https://github.com/Twingate/kubernetes-operator/pull/208),
  [`7baa616`](https://github.com/Twingate/kubernetes-operator/commit/7baa616162f3deadb500e08184f6277fb1deb34b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google.golang.org/protobuf from 1.31.0 to 1.33.0
  ([#194](https://github.com/Twingate/kubernetes-operator/pull/194),
  [`ca78968`](https://github.com/Twingate/kubernetes-operator/commit/ca78968f167c99fc1bcf4fa637e47a8c94bb3f2e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump mypy from 1.8.0 to 1.9.0 ([#196](https://github.com/Twingate/kubernetes-operator/pull/196),
  [`a07f4a8`](https://github.com/Twingate/kubernetes-operator/commit/a07f4a8cb510461ab93dda44c6ca8b465fcc1be1))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pre-commit from 3.6.2 to 3.7.0
  ([#220](https://github.com/Twingate/kubernetes-operator/pull/220),
  [`81239a5`](https://github.com/Twingate/kubernetes-operator/commit/81239a5aad9a8d2658d02f7190faf634aa06aebe))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.6.3 to 2.6.4
  ([#200](https://github.com/Twingate/kubernetes-operator/pull/200),
  [`b14c931`](https://github.com/Twingate/kubernetes-operator/commit/b14c9313215f90c40404a0bbd11d78fd116c6460))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 8.1.0 to 8.1.1 ([#197](https://github.com/Twingate/kubernetes-operator/pull/197),
  [`16687d8`](https://github.com/Twingate/kubernetes-operator/commit/16687d84fe0afc22e9cdcf116d7b3a79324f7b3f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest-cov from 4.1.0 to 5.0.0
  ([#219](https://github.com/Twingate/kubernetes-operator/pull/219),
  [`61e4cc5`](https://github.com/Twingate/kubernetes-operator/commit/61e4cc5ba73231d1cec6bf64c33d6aed372cf19f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.1.1 to 9.2.2
  ([#206](https://github.com/Twingate/kubernetes-operator/pull/206),
  [`eb122f7`](https://github.com/Twingate/kubernetes-operator/commit/eb122f7a46079f3fb867426a8b0e967c493f3478))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.2.2 to 9.3.0
  ([#209](https://github.com/Twingate/kubernetes-operator/pull/209),
  [`5f7b54f`](https://github.com/Twingate/kubernetes-operator/commit/5f7b54fad1811007026b7bb04a6da6134644747b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.3.0 to 9.3.1
  ([#221](https://github.com/Twingate/kubernetes-operator/pull/221),
  [`224897d`](https://github.com/Twingate/kubernetes-operator/commit/224897d9b2b7b8ffba37ad3db90f31086229a220))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pyupgrade from 3.15.1 to 3.15.2
  ([#218](https://github.com/Twingate/kubernetes-operator/pull/218),
  [`5dc320a`](https://github.com/Twingate/kubernetes-operator/commit/5dc320a7a9be39383568eef335d6b1ff11ae2c00))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.3.1 to 0.3.3 ([#199](https://github.com/Twingate/kubernetes-operator/pull/199),
  [`033c0ff`](https://github.com/Twingate/kubernetes-operator/commit/033c0ff3c3be88c6df5f7298539cb2fc6ec4b0cb))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.3.3 to 0.3.4 ([#213](https://github.com/Twingate/kubernetes-operator/pull/213),
  [`15ed2b9`](https://github.com/Twingate/kubernetes-operator/commit/15ed2b931cfac64a81ec79f25e1fed822601cf7a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-croniter from 2.0.0.20240106 to 2.0.0.20240318
  ([#203](https://github.com/Twingate/kubernetes-operator/pull/203),
  [`cf5d0e3`](https://github.com/Twingate/kubernetes-operator/commit/cf5d0e35bfbfad0f278c7da66e09702dbb001d95))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-croniter from 2.0.0.20240318 to 2.0.0.20240321
  ([#210](https://github.com/Twingate/kubernetes-operator/pull/210),
  [`17790dd`](https://github.com/Twingate/kubernetes-operator/commit/17790dd9f4b1161f4347632dd7fc4b4d5d2def39))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.31.0.20240218 to 2.31.0.20240311
  ([#204](https://github.com/Twingate/kubernetes-operator/pull/204),
  [`ad48466`](https://github.com/Twingate/kubernetes-operator/commit/ad484663ff3f8448cfae549ca0454a08ac5327fb))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Integration test for old pod migration
  ([#190](https://github.com/Twingate/kubernetes-operator/pull/190),
  [`2dff2b3`](https://github.com/Twingate/kubernetes-operator/commit/2dff2b36c960bddaa3e448a94ed68415a8ef4cb9))

- Temporary disable poetry package-mode until dependabot upgrades
  ([`7b4c207`](https://github.com/Twingate/kubernetes-operator/commit/7b4c20730574983b2e08fddc71a0ca6105e3bb9c))

- Upgrade Go to 1.22.0 and setup dependabot
  ([#205](https://github.com/Twingate/kubernetes-operator/pull/205),
  [`6f53ebf`](https://github.com/Twingate/kubernetes-operator/commit/6f53ebf45a52a76b6fb35b8d190a51bf827e6c2d))


## v0.6.2 (2024-03-11)

### Bug Fixes

- Resource restricted policy should allow empty ports
  ([#193](https://github.com/Twingate/kubernetes-operator/pull/193),
  [`e9aec7d`](https://github.com/Twingate/kubernetes-operator/commit/e9aec7d9ee7be6944d4c69b8d9d73107d3a38df5))


## v0.6.1 (2024-03-07)

### Bug Fixes

- Fix k8s_force_delete_pod finalizers removal
  ([#189](https://github.com/Twingate/kubernetes-operator/pull/189),
  [`5b2a8f3`](https://github.com/Twingate/kubernetes-operator/commit/5b2a8f396a7abbacf958c37406b2c4dd6dc6bd6a))

### Chores

- Bump ruff from 0.3.0 to 0.3.1 ([#187](https://github.com/Twingate/kubernetes-operator/pull/187),
  [`b0a282d`](https://github.com/Twingate/kubernetes-operator/commit/b0a282d2f6ce586f52cc3e00ed1a61a887e8e577))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Set poetry to package-mode = false
  ([#188](https://github.com/Twingate/kubernetes-operator/pull/188),
  [`f91f57a`](https://github.com/Twingate/kubernetes-operator/commit/f91f57a17905d648041b0099dc5568700440a121))


## v0.6.0 (2024-03-06)

### Bug Fixes

- Connector pod updates "Forbidden" error
  ([#184](https://github.com/Twingate/kubernetes-operator/pull/184),
  [`8096e62`](https://github.com/Twingate/kubernetes-operator/commit/8096e62c89d238035653f9e57ded8ece028505f6))

### Chores

- Bump google-cloud-artifact-registry from 1.11.2 to 1.11.3
  ([#186](https://github.com/Twingate/kubernetes-operator/pull/186),
  [`4b72d8b`](https://github.com/Twingate/kubernetes-operator/commit/4b72d8bcdc9cb998f201201a53f02453b8124079))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 8.0.2 to 8.1.0 ([#182](https://github.com/Twingate/kubernetes-operator/pull/182),
  [`13e479b`](https://github.com/Twingate/kubernetes-operator/commit/13e479bce27f4394e5377b219e4b8b0f7c3deb61))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest-factoryboy from 2.6.0 to 2.7.0
  ([#185](https://github.com/Twingate/kubernetes-operator/pull/185),
  [`22b7f84`](https://github.com/Twingate/kubernetes-operator/commit/22b7f8413696af873258243ba58e2126fa95e43a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Upgrade Poetry to 1.8.1 ([#181](https://github.com/Twingate/kubernetes-operator/pull/181),
  [`2f490f8`](https://github.com/Twingate/kubernetes-operator/commit/2f490f8e833bb32d50eabd8f5d5df198f174e812))

- Upgrade Poetry to latest 1.8.2 ([#183](https://github.com/Twingate/kubernetes-operator/pull/183),
  [`128de82`](https://github.com/Twingate/kubernetes-operator/commit/128de8227d303e47dbf127f64aaef9114439bee1))

### Features

- Improved TwingateConnector reconciliation
  ([#180](https://github.com/Twingate/kubernetes-operator/pull/180),
  [`e0a4f25`](https://github.com/Twingate/kubernetes-operator/commit/e0a4f25c14f706de4e6149e302d61e41d6515a68))


## v0.5.0 (2024-03-01)

### Bug Fixes

- Add status and logs to `twingate_connector_resume`
  ([#168](https://github.com/Twingate/kubernetes-operator/pull/168),
  [`13495f0`](https://github.com/Twingate/kubernetes-operator/commit/13495f0ade55b07728accde0080b34f6bbe84877))

- Deleting an item already deleted on Twingate Admin should not fail
  ([#160](https://github.com/Twingate/kubernetes-operator/pull/160),
  [`3cd447f`](https://github.com/Twingate/kubernetes-operator/commit/3cd447f1caa07772b8d821c34d96de88c159724d))

- Improved `twingate_connector_recreate_pod` logic
  ([#179](https://github.com/Twingate/kubernetes-operator/pull/179),
  [`fd3f533`](https://github.com/Twingate/kubernetes-operator/commit/fd3f533dfc2d4a67a8679dd2666c249f0869f500))

- Label_connector_pod_deleted isnt set to false after pod recreated
  ([#177](https://github.com/Twingate/kubernetes-operator/pull/177),
  [`f3d6865`](https://github.com/Twingate/kubernetes-operator/commit/f3d686599e43a175c10d3a8032187d47e74e61dd))

- Limit twingate_resource_access_update scope to spec
  ([#175](https://github.com/Twingate/kubernetes-operator/pull/175),
  [`75ff3f0`](https://github.com/Twingate/kubernetes-operator/commit/75ff3f05a0159dff0d3f454141baf546cbc0eb1f))

- Reduce update scope for `twingate_resource_update`
  ([#176](https://github.com/Twingate/kubernetes-operator/pull/176),
  [`c947fba`](https://github.com/Twingate/kubernetes-operator/commit/c947fba876047317f2921e0bbb52654fded66e38))

- Twingate connector doesnt handle pod deletion on resume
  ([#162](https://github.com/Twingate/kubernetes-operator/pull/162),
  [`7fbc24b`](https://github.com/Twingate/kubernetes-operator/commit/7fbc24b0d41a5b47dc397851c10911aac94bb777))

### Chores

- Bump autoflake from 2.2.1 to 2.3.0
  ([#150](https://github.com/Twingate/kubernetes-operator/pull/150),
  [`9e0c5d1`](https://github.com/Twingate/kubernetes-operator/commit/9e0c5d1e78ebaa31dd12a34a5bff525577379f87))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump croniter from 2.0.1 to 2.0.2
  ([#172](https://github.com/Twingate/kubernetes-operator/pull/172),
  [`d8e2e88`](https://github.com/Twingate/kubernetes-operator/commit/d8e2e88facd234d65067e14f035b991bae803574))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google-cloud-artifact-registry from 1.11.1 to 1.11.2
  ([#158](https://github.com/Twingate/kubernetes-operator/pull/158),
  [`2e6a03c`](https://github.com/Twingate/kubernetes-operator/commit/2e6a03c2a4dc4f3d151f45eef1b85407a6bf11f5))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.9.14 to 3.9.15
  ([#163](https://github.com/Twingate/kubernetes-operator/pull/163),
  [`c8550e5`](https://github.com/Twingate/kubernetes-operator/commit/c8550e5647ea4be80113e904c79ecb35f458e822))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pre-commit from 3.6.1 to 3.6.2
  ([#154](https://github.com/Twingate/kubernetes-operator/pull/154),
  [`9c188aa`](https://github.com/Twingate/kubernetes-operator/commit/9c188aadc3bdcb03712a948b925d69eb941532f0))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.6.1 to 2.6.2
  ([#166](https://github.com/Twingate/kubernetes-operator/pull/166),
  [`3601ec0`](https://github.com/Twingate/kubernetes-operator/commit/3601ec00173ca9fb4905e73856a919bd42a25d6f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.6.2 to 2.6.3
  ([#167](https://github.com/Twingate/kubernetes-operator/pull/167),
  [`cacfec8`](https://github.com/Twingate/kubernetes-operator/commit/cacfec801bd634633aa8156047a05f9c452e541f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.1.0 to 2.2.0
  ([#151](https://github.com/Twingate/kubernetes-operator/pull/151),
  [`c3ccbe4`](https://github.com/Twingate/kubernetes-operator/commit/c3ccbe47da50c7b20edf2d986b130f9d886a6ef6))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.2.0 to 2.2.1
  ([#157](https://github.com/Twingate/kubernetes-operator/pull/157),
  [`830b6ac`](https://github.com/Twingate/kubernetes-operator/commit/830b6ac04ed30b249ec87e5cd1ba8af346af7c3b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 8.0.0 to 8.0.1 ([#155](https://github.com/Twingate/kubernetes-operator/pull/155),
  [`a8fcd50`](https://github.com/Twingate/kubernetes-operator/commit/a8fcd50e1da8c83f0bab1dcd6afd00f9f49cbd90))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 8.0.1 to 8.0.2 ([#165](https://github.com/Twingate/kubernetes-operator/pull/165),
  [`dc7e2aa`](https://github.com/Twingate/kubernetes-operator/commit/dc7e2aa26b096365fad7d1a580df387e6a6819e9))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.1.0 to 9.1.1
  ([#164](https://github.com/Twingate/kubernetes-operator/pull/164),
  [`76a0e07`](https://github.com/Twingate/kubernetes-operator/commit/76a0e07ac378c94e32284a06ef044049806d2886))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pyupgrade from 3.15.0 to 3.15.1
  ([#153](https://github.com/Twingate/kubernetes-operator/pull/153),
  [`fdfae86`](https://github.com/Twingate/kubernetes-operator/commit/fdfae86e8aff7a3a25873dc53f4c2cbdbc49a5fc))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.2.1 to 0.2.2 ([#152](https://github.com/Twingate/kubernetes-operator/pull/152),
  [`17f3017`](https://github.com/Twingate/kubernetes-operator/commit/17f30173d39d70cefeabd6d1a3d5c4fb1b810a78))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.2.2 to 0.3.0 ([#178](https://github.com/Twingate/kubernetes-operator/pull/178),
  [`918311b`](https://github.com/Twingate/kubernetes-operator/commit/918311b74ad654c90205fe34acc93553ab654f79))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

- Bump types-requests from 2.31.0.20240125 to 2.31.0.20240218
  ([#149](https://github.com/Twingate/kubernetes-operator/pull/149),
  [`e2e75b8`](https://github.com/Twingate/kubernetes-operator/commit/e2e75b8a1d6782baa2fcd6faa814ee63e845c100))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Pydantic deprecated .dict() for .model_dump()
  ([#171](https://github.com/Twingate/kubernetes-operator/pull/171),
  [`065c146`](https://github.com/Twingate/kubernetes-operator/commit/065c14687389e0de66575709d5b05e6403f55e39))

- Stalebot is deprecated. Move to actions/stale@v9
  ([#147](https://github.com/Twingate/kubernetes-operator/pull/147),
  [`94dce35`](https://github.com/Twingate/kubernetes-operator/commit/94dce35289d97e1c2674c3530d7418fe870b55e1))

- Switch from Black to Ruff Formatter
  ([#148](https://github.com/Twingate/kubernetes-operator/pull/148),
  [`1b822ae`](https://github.com/Twingate/kubernetes-operator/commit/1b822ae23be0cc7ec0cc4b5dffccf52c332dd696))

### Features

- Add `hasStatusNotificationsEnabled` to `TwingateConnector`
  ([#170](https://github.com/Twingate/kubernetes-operator/pull/170),
  [`f03f851`](https://github.com/Twingate/kubernetes-operator/commit/f03f851bdc1b9cf7f59e618205a5c3ae3baf55f5))


## v0.4.0 (2024-02-15)

### Bug Fixes

- Added `twingate_connector_image_update` to handle `image` updates
  ([#131](https://github.com/Twingate/kubernetes-operator/pull/131),
  [`25f2753`](https://github.com/Twingate/kubernetes-operator/commit/25f27537eb292b632163978a16c23b3053b0e637))

- Disable healthcheck access logs ([#135](https://github.com/Twingate/kubernetes-operator/pull/135),
  [`ad8eaba`](https://github.com/Twingate/kubernetes-operator/commit/ad8eabac03313d60959f9dc9ac48308a5114fa82))

- Fix resource `protocols` diffing and serialization
  ([#146](https://github.com/Twingate/kubernetes-operator/pull/146),
  [`7c9407e`](https://github.com/Twingate/kubernetes-operator/commit/7c9407e52185129201cf79a7bf5d6551711a16f9))

### Chores

- Bump actions/cache from 3 to 4 ([#143](https://github.com/Twingate/kubernetes-operator/pull/143),
  [`a6e2e9a`](https://github.com/Twingate/kubernetes-operator/commit/a6e2e9a39065811ec39859466a30258a4cfe7b10))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump actions/setup-go from 4 to 5
  ([#141](https://github.com/Twingate/kubernetes-operator/pull/141),
  [`770d518`](https://github.com/Twingate/kubernetes-operator/commit/770d5188aa3ea6e9b6920bfb858fc2580a8b868c))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump actions/setup-python from 4 to 5
  ([#140](https://github.com/Twingate/kubernetes-operator/pull/140),
  [`eae1613`](https://github.com/Twingate/kubernetes-operator/commit/eae161335f08308d128eb32924dadf991da15cf1))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump black from 24.1.1 to 24.2.0
  ([#132](https://github.com/Twingate/kubernetes-operator/pull/132),
  [`9794e04`](https://github.com/Twingate/kubernetes-operator/commit/9794e0402c53fa92cd71161ee848edef67c1d69d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump crazy-max/ghaction-github-runtime from 2 to 3
  ([#138](https://github.com/Twingate/kubernetes-operator/pull/138),
  [`2833ea9`](https://github.com/Twingate/kubernetes-operator/commit/2833ea953889d943b36d6ea28b97996cfecdd1f4))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump danger/danger-js from 11.3.0 to 11.3.1
  ([#137](https://github.com/Twingate/kubernetes-operator/pull/137),
  [`f8d91fe`](https://github.com/Twingate/kubernetes-operator/commit/f8d91fee7007c13c58bb6f07e204cd8769f193a7))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google-cloud-artifact-registry from 1.10.0 to 1.11.0
  ([#112](https://github.com/Twingate/kubernetes-operator/pull/112),
  [`f1d74c7`](https://github.com/Twingate/kubernetes-operator/commit/f1d74c78ea665b0beaf4fff178b0760054d99a94))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google-cloud-artifact-registry from 1.11.0 to 1.11.1
  ([#125](https://github.com/Twingate/kubernetes-operator/pull/125),
  [`dc9c3e2`](https://github.com/Twingate/kubernetes-operator/commit/dc9c3e27492adc22b98869f4a33f83614b8f39d8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ncipollo/release-action from 1.13.0 to 1.14.0
  ([#139](https://github.com/Twingate/kubernetes-operator/pull/139),
  [`5ee2ab5`](https://github.com/Twingate/kubernetes-operator/commit/5ee2ab540dafd0ea2a9b405d636e45e33d0a451e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.9.12 to 3.9.13
  ([#115](https://github.com/Twingate/kubernetes-operator/pull/115),
  [`c15718b`](https://github.com/Twingate/kubernetes-operator/commit/c15718b4557442a0c672c4cbff208c50986dc486))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.9.13 to 3.9.14
  ([#134](https://github.com/Twingate/kubernetes-operator/pull/134),
  [`bed5200`](https://github.com/Twingate/kubernetes-operator/commit/bed5200e8eb370ae3fa856a89fcbcafca1c24038))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pre-commit from 3.6.0 to 3.6.1
  ([#127](https://github.com/Twingate/kubernetes-operator/pull/127),
  [`b3de58d`](https://github.com/Twingate/kubernetes-operator/commit/b3de58ddbda647f5d2f222ee559117e42bba958b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.6.0 to 2.6.1
  ([#117](https://github.com/Twingate/kubernetes-operator/pull/117),
  [`39d499d`](https://github.com/Twingate/kubernetes-operator/commit/39d499d684694abd5df762834b7e6a57b81ed9fb))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 7.4.4 to 8.0.0 ([#118](https://github.com/Twingate/kubernetes-operator/pull/118),
  [`0c46fc5`](https://github.com/Twingate/kubernetes-operator/commit/0c46fc5cca7a3459df1093c47dc2d76408d0ef31))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest-sugar from 0.9.7 to 1.0.0
  ([#113](https://github.com/Twingate/kubernetes-operator/pull/113),
  [`6671930`](https://github.com/Twingate/kubernetes-operator/commit/667193002e882ec0d30bf7006e964d5ac9569338))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 8.7.0 to 9.0.3
  ([#126](https://github.com/Twingate/kubernetes-operator/pull/126),
  [`7c4cd35`](https://github.com/Twingate/kubernetes-operator/commit/7c4cd3532170c33a7a5b73d8d99cb9c293e08695))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 9.0.3 to 9.1.0
  ([#142](https://github.com/Twingate/kubernetes-operator/pull/142),
  [`5d95517`](https://github.com/Twingate/kubernetes-operator/commit/5d9551783f2b2979405233eff6c115f6fcc6ce44))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump responses from 0.24.1 to 0.25.0
  ([#133](https://github.com/Twingate/kubernetes-operator/pull/133),
  [`9d01e7c`](https://github.com/Twingate/kubernetes-operator/commit/9d01e7c1287626b23cb706272a2e1c98ba84e560))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.1.15 to 0.2.0 ([#114](https://github.com/Twingate/kubernetes-operator/pull/114),
  [`88d5dc0`](https://github.com/Twingate/kubernetes-operator/commit/88d5dc0858cd6dcb512b6dedd00181178d268a33))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.2.0 to 0.2.1 ([#116](https://github.com/Twingate/kubernetes-operator/pull/116),
  [`028a5e8`](https://github.com/Twingate/kubernetes-operator/commit/028a5e8e227b3f29c73e7fca340d17f4a93ff729))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump syrupy from 4.6.0 to 4.6.1 ([#119](https://github.com/Twingate/kubernetes-operator/pull/119),
  [`378f7fc`](https://github.com/Twingate/kubernetes-operator/commit/378f7fcaea1d7208c43612f34c2ef29990c8abe5))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Monitor and update github actions
  ([`98f48f9`](https://github.com/Twingate/kubernetes-operator/commit/98f48f9b6c5aa1aaa2a67edc8815775b2d527de3))

- Upgrade Poetry to 1.7.1 ([#144](https://github.com/Twingate/kubernetes-operator/pull/144),
  [`fd18505`](https://github.com/Twingate/kubernetes-operator/commit/fd18505a98047a4e65b8bbc0eb24f0520f7d1462))

### Features

- Add podLabels ([#129](https://github.com/Twingate/kubernetes-operator/pull/129),
  [`642af6a`](https://github.com/Twingate/kubernetes-operator/commit/642af6a1bb87f696ff07557ab78de63eefa40b82))

- Add support for priorityClassName
  ([#128](https://github.com/Twingate/kubernetes-operator/pull/128),
  [`e2d233c`](https://github.com/Twingate/kubernetes-operator/commit/e2d233c86569ec38ce905f1d8e244fff94090b60))


## v0.3.0 (2024-01-30)

### Build System

- Make CHANGELOG generation nicer ([#98](https://github.com/Twingate/kubernetes-operator/pull/98),
  [`c13b35b`](https://github.com/Twingate/kubernetes-operator/commit/c13b35bca740a24df2dcf510ba09fcf1bd62d1b5))

### Chores

- Bump aiohttp from 3.9.0 to 3.9.2
  ([#109](https://github.com/Twingate/kubernetes-operator/pull/109),
  [`5576218`](https://github.com/Twingate/kubernetes-operator/commit/557621885ea921f82bc461cdfff85795c03e6668))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump bandit from 1.7.6 to 1.7.7 ([#105](https://github.com/Twingate/kubernetes-operator/pull/105),
  [`f9a682e`](https://github.com/Twingate/kubernetes-operator/commit/f9a682e475abd872e572bfac45e62f7324296bb5))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump black from 23.12.1 to 24.1.1
  ([#108](https://github.com/Twingate/kubernetes-operator/pull/108),
  [`f48e140`](https://github.com/Twingate/kubernetes-operator/commit/f48e14039c02c08e191c6d3438f812b0ed4f84d3))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

- Bump kopf from 1.36.2 to 1.37.1 ([#101](https://github.com/Twingate/kubernetes-operator/pull/101),
  [`1c81f10`](https://github.com/Twingate/kubernetes-operator/commit/1c81f10aa9d25eeda25e8f8fa29942eaf3a9a006))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump orjson from 3.9.10 to 3.9.12 ([#99](https://github.com/Twingate/kubernetes-operator/pull/99),
  [`03455ed`](https://github.com/Twingate/kubernetes-operator/commit/03455ed4b77bb86b95046b1b377315ae45c14eb1))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.5.3 to 2.6.0
  ([#111](https://github.com/Twingate/kubernetes-operator/pull/111),
  [`b875c14`](https://github.com/Twingate/kubernetes-operator/commit/b875c1453f3a158e52dbb29eb8a8f3f39232518d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.1.13 to 0.1.14 ([#100](https://github.com/Twingate/kubernetes-operator/pull/100),
  [`32c783a`](https://github.com/Twingate/kubernetes-operator/commit/32c783a2f3277bfba7472f409245237a8d6ae51d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.1.14 to 0.1.15 ([#110](https://github.com/Twingate/kubernetes-operator/pull/110),
  [`397c59d`](https://github.com/Twingate/kubernetes-operator/commit/397c59d50047606b2af473cc20af7405e22d487e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.31.0.20240106 to 2.31.0.20240125
  ([#106](https://github.com/Twingate/kubernetes-operator/pull/106),
  [`76b078c`](https://github.com/Twingate/kubernetes-operator/commit/76b078c4d77d9a05cdf7193101899154442fc339))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Features

- Add relevant security context to run as non root
  ([#103](https://github.com/Twingate/kubernetes-operator/pull/103),
  [`c1cdfb7`](https://github.com/Twingate/kubernetes-operator/commit/c1cdfb7c664aff1f15ea274e8f12a7c945811b33))

- Add seccompProfile by default ([#104](https://github.com/Twingate/kubernetes-operator/pull/104),
  [`e3ef8d6`](https://github.com/Twingate/kubernetes-operator/commit/e3ef8d6ad9350ccdf95dcf3eb022ed73e845c530))


## v0.2.0 (2024-01-18)

### Bug Fixes

- Allow setting remote network by name - TwingateSettings failure
  ([#93](https://github.com/Twingate/kubernetes-operator/pull/93),
  [`a958588`](https://github.com/Twingate/kubernetes-operator/commit/a95858881bc18f7f4a3c46c333d2ca6351452520))

- Chore, build changes should change patch
  ([#36](https://github.com/Twingate/kubernetes-operator/pull/36),
  [`cfda90b`](https://github.com/Twingate/kubernetes-operator/commit/cfda90bda4476f4d94d60755d6e522025660b545))

- Clusterrole definition - create\delete pods and secrets required by Connector functionality
  ([#94](https://github.com/Twingate/kubernetes-operator/pull/94),
  [`d4674fc`](https://github.com/Twingate/kubernetes-operator/commit/d4674fc8ae8e4a702806e1b63c6571abc4f6c936))

- Gql.client can't be singleton as its not thread-safe
  ([#96](https://github.com/Twingate/kubernetes-operator/pull/96),
  [`f137124`](https://github.com/Twingate/kubernetes-operator/commit/f137124489e9705f6b7aba93714e3f90d31b8a04))

- Test_remote_network_name_gets_network_id
  ([#97](https://github.com/Twingate/kubernetes-operator/pull/97),
  [`9c0afb9`](https://github.com/Twingate/kubernetes-operator/commit/9c0afb9167087b9037e6cec92c2d8d78a75bc3a1))

- Typo in class name - TwingateRety -> TwingateRetry
  ([#95](https://github.com/Twingate/kubernetes-operator/pull/95),
  [`a9d8882`](https://github.com/Twingate/kubernetes-operator/commit/a9d88827a72e95cd28d8026ffc38bbf5f942e370))

### Build System

- Replace pydocstyle with ruff ([#35](https://github.com/Twingate/kubernetes-operator/pull/35),
  [`b771c7a`](https://github.com/Twingate/kubernetes-operator/commit/b771c7a659525f9414964606189ec4ff2dd2384e))

### Chores

- Adding the docker vulnerability monitor
  ([#30](https://github.com/Twingate/kubernetes-operator/pull/30),
  [`b9af2ec`](https://github.com/Twingate/kubernetes-operator/commit/b9af2ecb4189d466c19b6fd86c104380e182b201))

Co-authored-by: Eran Kampf <eran@ekampf.com>

Co-authored-by: Eran Kampf <205185+ekampf@users.noreply.github.com>

- Bump aiohttp from 3.8.5 to 3.8.6 ([#45](https://github.com/Twingate/kubernetes-operator/pull/45),
  [`bf7fcbd`](https://github.com/Twingate/kubernetes-operator/commit/bf7fcbdfc6baebe091f37496ad04898f9e965c78))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump aiohttp from 3.8.6 to 3.9.0 ([#52](https://github.com/Twingate/kubernetes-operator/pull/52),
  [`bae78a0`](https://github.com/Twingate/kubernetes-operator/commit/bae78a03ec00697334d1980a208f691612ce2c61))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump bandit from 1.7.5 to 1.7.6 ([#65](https://github.com/Twingate/kubernetes-operator/pull/65),
  [`502f74d`](https://github.com/Twingate/kubernetes-operator/commit/502f74d2d16856f115621e0b99131844bf15a44e))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump black from 23.10.1 to 23.11.0
  ([#33](https://github.com/Twingate/kubernetes-operator/pull/33),
  [`28284ad`](https://github.com/Twingate/kubernetes-operator/commit/28284ad7ead047500e3b0381578b70f844c547e1))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump black from 23.11.0 to 23.12.0
  ([#67](https://github.com/Twingate/kubernetes-operator/pull/67),
  [`1725941`](https://github.com/Twingate/kubernetes-operator/commit/1725941cd13c8d7d3368ad036a97ba9da5d334d9))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump black from 23.12.0 to 23.12.1
  ([#80](https://github.com/Twingate/kubernetes-operator/pull/80),
  [`fb2bff3`](https://github.com/Twingate/kubernetes-operator/commit/fb2bff31c06e8f9c78b86f0ad034ec14def2302b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump gitpython from 3.1.37 to 3.1.41
  ([#88](https://github.com/Twingate/kubernetes-operator/pull/88),
  [`cf03bb0`](https://github.com/Twingate/kubernetes-operator/commit/cf03bb0457b541b4b900941da40e3a3bdfe0fe52))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump golang.org/x/crypto from 0.14.0 to 0.17.0
  ([#74](https://github.com/Twingate/kubernetes-operator/pull/74),
  [`33d5f7e`](https://github.com/Twingate/kubernetes-operator/commit/33d5f7edd403808bcd98516c9d8693f1137f1bc3))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump google-cloud-artifact-registry from 1.9.0 to 1.10.0
  ([#61](https://github.com/Twingate/kubernetes-operator/pull/61),
  [`2196492`](https://github.com/Twingate/kubernetes-operator/commit/21964921d81884aeca6468e02a5abda3d44c651d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump gql from 3.4.1 to 3.5.0 ([#83](https://github.com/Twingate/kubernetes-operator/pull/83),
  [`2134808`](https://github.com/Twingate/kubernetes-operator/commit/2134808d4eef1ddbda618eb04329166fee860a89))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

- Bump isort from 5.12.0 to 5.13.0 ([#64](https://github.com/Twingate/kubernetes-operator/pull/64),
  [`36061f2`](https://github.com/Twingate/kubernetes-operator/commit/36061f2bfd7fb8887d1c188a380d6ceb65fa3e0d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump isort from 5.13.0 to 5.13.1 ([#66](https://github.com/Twingate/kubernetes-operator/pull/66),
  [`3611312`](https://github.com/Twingate/kubernetes-operator/commit/3611312a5644ea3f6ef91a2408e5990dcc3e9514))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump isort from 5.13.1 to 5.13.2 ([#69](https://github.com/Twingate/kubernetes-operator/pull/69),
  [`5515058`](https://github.com/Twingate/kubernetes-operator/commit/5515058c4db8cddd648a267632ef1fbed55e12db))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump jinja2 from 3.1.2 to 3.1.3 ([#89](https://github.com/Twingate/kubernetes-operator/pull/89),
  [`290cbbb`](https://github.com/Twingate/kubernetes-operator/commit/290cbbba9cff2bf68aec0a1eef0301a87a45f133))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump kubernetes from 28.1.0 to 29.0.0
  ([#86](https://github.com/Twingate/kubernetes-operator/pull/86),
  [`36af9e5`](https://github.com/Twingate/kubernetes-operator/commit/36af9e5bec36eba988f7400491f091dfb325e606))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump mypy from 1.6.1 to 1.7.0 ([#37](https://github.com/Twingate/kubernetes-operator/pull/37),
  [`858efb0`](https://github.com/Twingate/kubernetes-operator/commit/858efb0452867e1e45e47595e5e72c63be71ab77))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump mypy from 1.7.0 to 1.7.1 ([#51](https://github.com/Twingate/kubernetes-operator/pull/51),
  [`2da6a12`](https://github.com/Twingate/kubernetes-operator/commit/2da6a1220a1978f81d41cd70113d4b17b0b426c3))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump mypy from 1.7.1 to 1.8.0 ([#77](https://github.com/Twingate/kubernetes-operator/pull/77),
  [`3a7fd5d`](https://github.com/Twingate/kubernetes-operator/commit/3a7fd5df943fe1ed43d88ee790341d79e0f38d75))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pendulum from 2.1.2 to 3.0.0 ([#73](https://github.com/Twingate/kubernetes-operator/pull/73),
  [`982e747`](https://github.com/Twingate/kubernetes-operator/commit/982e747272168476d04d4658809096c05d95af9f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pre-commit from 3.5.0 to 3.6.0
  ([#63](https://github.com/Twingate/kubernetes-operator/pull/63),
  [`3eb9d07`](https://github.com/Twingate/kubernetes-operator/commit/3eb9d0757aad13bb376e7366859ec46c74984713))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.4.2 to 2.5.0 ([#43](https://github.com/Twingate/kubernetes-operator/pull/43),
  [`c2dddfb`](https://github.com/Twingate/kubernetes-operator/commit/c2dddfb048b4cfee7f392bc50284b60bd1f92970))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.5.0 to 2.5.1 ([#47](https://github.com/Twingate/kubernetes-operator/pull/47),
  [`b2a9df5`](https://github.com/Twingate/kubernetes-operator/commit/b2a9df5f413cbce69cef192dc9db3fd5e91463d2))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.5.1 to 2.5.2 ([#50](https://github.com/Twingate/kubernetes-operator/pull/50),
  [`132983d`](https://github.com/Twingate/kubernetes-operator/commit/132983dd171d8e1ed6794a16b76053c843bcdc2b))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic from 2.5.2 to 2.5.3 ([#76](https://github.com/Twingate/kubernetes-operator/pull/76),
  [`f994717`](https://github.com/Twingate/kubernetes-operator/commit/f994717041bef4947836e5690e38126dcf972163))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pydantic-settings from 2.0.3 to 2.1.0
  ([#44](https://github.com/Twingate/kubernetes-operator/pull/44),
  [`71b4c11`](https://github.com/Twingate/kubernetes-operator/commit/71b4c116e68a795c1c9974c298f011156c9e0c4a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 7.4.3 to 7.4.4 ([#81](https://github.com/Twingate/kubernetes-operator/pull/81),
  [`3a2c181`](https://github.com/Twingate/kubernetes-operator/commit/3a2c181ff9ea69db821159197a14591c43c3a6e8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 8.3.0 to 8.5.0
  ([#60](https://github.com/Twingate/kubernetes-operator/pull/60),
  [`973f0de`](https://github.com/Twingate/kubernetes-operator/commit/973f0de3cbddb3170640b3ac8ac0c2db6ddcdcf0))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 8.5.0 to 8.5.1
  ([#68](https://github.com/Twingate/kubernetes-operator/pull/68),
  [`eec07cb`](https://github.com/Twingate/kubernetes-operator/commit/eec07cb860f0ed046b78f70355b91942655f9c0c))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 8.5.1 to 8.5.2
  ([#75](https://github.com/Twingate/kubernetes-operator/pull/75),
  [`1ce66db`](https://github.com/Twingate/kubernetes-operator/commit/1ce66db7ed428d9591188e178528a91d444ba6d8))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 8.5.2 to 8.7.0
  ([#78](https://github.com/Twingate/kubernetes-operator/pull/78),
  [`15daa70`](https://github.com/Twingate/kubernetes-operator/commit/15daa702e9620fd4121ec859ab7f397958f1e756))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump responses from 0.23.3 to 0.24.0
  ([#29](https://github.com/Twingate/kubernetes-operator/pull/29),
  [`79e169a`](https://github.com/Twingate/kubernetes-operator/commit/79e169a3e8c4d392eb3e1a0352e2c0bafba3ca66))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

- Bump responses from 0.24.0 to 0.24.1
  ([#46](https://github.com/Twingate/kubernetes-operator/pull/46),
  [`b9e62a2`](https://github.com/Twingate/kubernetes-operator/commit/b9e62a206c904fb82eca7723ebf6432695dbefee))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.1.11 to 0.1.12 ([#90](https://github.com/Twingate/kubernetes-operator/pull/90),
  [`e81271b`](https://github.com/Twingate/kubernetes-operator/commit/e81271bbcf3f12bfbf9bac29b186367520ca5ffb))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.1.12 to 0.1.13 ([#91](https://github.com/Twingate/kubernetes-operator/pull/91),
  [`35b23ad`](https://github.com/Twingate/kubernetes-operator/commit/35b23ade45cf80ceb82e20a9c82987cd8035b8f1))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.1.3 to 0.1.4 ([#31](https://github.com/Twingate/kubernetes-operator/pull/31),
  [`d218bfe`](https://github.com/Twingate/kubernetes-operator/commit/d218bfe2683a133e1b52bd1878066cdda66ac06f))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <eran@ekampf.com>

- Bump ruff from 0.1.4 to 0.1.5 ([#34](https://github.com/Twingate/kubernetes-operator/pull/34),
  [`363f50a`](https://github.com/Twingate/kubernetes-operator/commit/363f50a5899b3949602a4a0db2179333698bf9cb))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.1.5 to 0.1.6 ([#49](https://github.com/Twingate/kubernetes-operator/pull/49),
  [`74042b6`](https://github.com/Twingate/kubernetes-operator/commit/74042b67176454e434a134659ac1781fba70a2a5))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.1.6 to 0.1.7 ([#59](https://github.com/Twingate/kubernetes-operator/pull/59),
  [`64fe08d`](https://github.com/Twingate/kubernetes-operator/commit/64fe08d6d35031656cd1ecfb384cf4ea9d94940a))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.1.7 to 0.1.8 ([#70](https://github.com/Twingate/kubernetes-operator/pull/70),
  [`af3370c`](https://github.com/Twingate/kubernetes-operator/commit/af3370c3c6ac1360b96039a0a3b2e89c728b1160))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.1.8 to 0.1.9 ([#79](https://github.com/Twingate/kubernetes-operator/pull/79),
  [`b22629d`](https://github.com/Twingate/kubernetes-operator/commit/b22629ddcbe876b8c3b39701108ccc83d57e0dc5))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.1.9 to 0.1.11 ([#82](https://github.com/Twingate/kubernetes-operator/pull/82),
  [`6d3083c`](https://github.com/Twingate/kubernetes-operator/commit/6d3083cf6f81280cc968ecffc343bc0cce7e0208))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-croniter from 2.0.0.0 to 2.0.0.20240106
  ([#85](https://github.com/Twingate/kubernetes-operator/pull/85),
  [`c247fd7`](https://github.com/Twingate/kubernetes-operator/commit/c247fd79bf46196f3e33e8beb5de9b8be3cc70ad))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump types-requests from 2.31.0.6 to 2.31.0.20240106
  ([#87](https://github.com/Twingate/kubernetes-operator/pull/87),
  [`5739c52`](https://github.com/Twingate/kubernetes-operator/commit/5739c52b3b51588736bb376c08ae8d1211860d01))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Sort lines on pyproject dependencies
  ([#39](https://github.com/Twingate/kubernetes-operator/pull/39),
  [`62c1338`](https://github.com/Twingate/kubernetes-operator/commit/62c133801a9f744988e80ca939815f642bc0c6d1))

### Documentation

- Add descriptions to CRD fields ([#48](https://github.com/Twingate/kubernetes-operator/pull/48),
  [`bdd6110`](https://github.com/Twingate/kubernetes-operator/commit/bdd6110c7a49a24d069090bc9a3927bc34bf3127))

### Features

- Add allowPrivilegeEscalation: false to values.yaml
  ([#92](https://github.com/Twingate/kubernetes-operator/pull/92),
  [`55a4ce2`](https://github.com/Twingate/kubernetes-operator/commit/55a4ce2e7a15ceb74d64c2997f7943779430aed3))

- Add GCP Support for connector imagePolicy
  ([#54](https://github.com/Twingate/kubernetes-operator/pull/54),
  [`0b5b84f`](https://github.com/Twingate/kubernetes-operator/commit/0b5b84f64999b1ced7a6a734ec8673319c0cf16d))

- Allow customizing connector logLevel
  ([#58](https://github.com/Twingate/kubernetes-operator/pull/58),
  [`b2323a8`](https://github.com/Twingate/kubernetes-operator/commit/b2323a845c71e2f3911b2a36e925345061740b24))

- Allow setting remote network by name
  ([#84](https://github.com/Twingate/kubernetes-operator/pull/84),
  [`835c4c2`](https://github.com/Twingate/kubernetes-operator/commit/835c4c2bd55c07a602bfdbfff8854be47e4946bc))

- Allow specifying API Key via reference to an external Secret
  ([#72](https://github.com/Twingate/kubernetes-operator/pull/72),
  [`a028068`](https://github.com/Twingate/kubernetes-operator/commit/a0280684cf9d6302ba460e1f99d76e0dd15b8e32))

- Twingateconnector object (auto provision and update)
  ([#27](https://github.com/Twingate/kubernetes-operator/pull/27),
  [`7a135f2`](https://github.com/Twingate/kubernetes-operator/commit/7a135f26d2e4cb6bcbdf4839ac76f62149443f1f))

### Testing

- Randomize test runs and fix errorsa
  ([#41](https://github.com/Twingate/kubernetes-operator/pull/41),
  [`f953678`](https://github.com/Twingate/kubernetes-operator/commit/f953678a610f5dbc0d4b65016aebf02372f225e8))

- Remove unused fixture ([#42](https://github.com/Twingate/kubernetes-operator/pull/42),
  [`6cd4d68`](https://github.com/Twingate/kubernetes-operator/commit/6cd4d68f924d051bbfec441ae31710a0e3b3dccb))

- Reorganize integration tests ([#28](https://github.com/Twingate/kubernetes-operator/pull/28),
  [`86a27e4`](https://github.com/Twingate/kubernetes-operator/commit/86a27e46b24c975b0a13497d67107d0e3fd6c632))

- Simplify integration tests setup ([#38](https://github.com/Twingate/kubernetes-operator/pull/38),
  [`d757085`](https://github.com/Twingate/kubernetes-operator/commit/d75708577a1d89e186fb08b4c887316d0b40fa56))

- Use pytest-factoryboy instead of defining factory fixtures manually
  ([#40](https://github.com/Twingate/kubernetes-operator/pull/40),
  [`8b3d012`](https://github.com/Twingate/kubernetes-operator/commit/8b3d0129a1cb4b403ea87d3dbb2ec2ca923c69b9))


## v0.1.2 (2023-11-01)

### Bug Fixes

- Change persistence layer - operator.twingate.com to just twingate.com
  ([#24](https://github.com/Twingate/kubernetes-operator/pull/24),
  [`d7ebd7b`](https://github.com/Twingate/kubernetes-operator/commit/d7ebd7bf624182430671989587c2c767018180a7))

### Documentation

- Improve development docs ([#25](https://github.com/Twingate/kubernetes-operator/pull/25),
  [`ebf8cdb`](https://github.com/Twingate/kubernetes-operator/commit/ebf8cdbbcc368636e9af76c8c7ed24233c2bf378))

### Testing

- Resourceaccess integration testing
  ([#23](https://github.com/Twingate/kubernetes-operator/pull/23),
  [`8aa5621`](https://github.com/Twingate/kubernetes-operator/commit/8aa5621aa02f1efc0fef1dc49fb1624b3309ee4f))

Co-authored-by: Eran Kampf <eran@ekampf.com>


## v0.1.1 (2023-10-30)

### Bug Fixes

- Resourceaccessspec.get_resource_ref_object fetching wrong version
  ([#20](https://github.com/Twingate/kubernetes-operator/pull/20),
  [`86b6557`](https://github.com/Twingate/kubernetes-operator/commit/86b6557107ea927ec0244ba91ccacb680aab9751))

Co-authored-by: semantic-release <semantic-release>


## v0.1.0 (2023-10-30)

### Bug Fixes

- Change persistence settings to use Twingate namespace
  ([#18](https://github.com/Twingate/kubernetes-operator/pull/18),
  [`41729d3`](https://github.com/Twingate/kubernetes-operator/commit/41729d342d95d00d6a1319e95ea8dfd4021a1228))

- Dev release tags ([#13](https://github.com/Twingate/kubernetes-operator/pull/13),
  [`28ad640`](https://github.com/Twingate/kubernetes-operator/commit/28ad6407a388c35b2cc521f1a43497f9a244fb9c))

- Fix helm chart + add log formatting
  ([#19](https://github.com/Twingate/kubernetes-operator/pull/19),
  [`9fb6675`](https://github.com/Twingate/kubernetes-operator/commit/9fb66755ecc6018d20e63988a305b1cbd0fb07b6))

### Build System

- Fix missing semantic-release dependency on release_dev step
  ([#14](https://github.com/Twingate/kubernetes-operator/pull/14),
  [`e07e364`](https://github.com/Twingate/kubernetes-operator/commit/e07e364b858bf4a125ee103ce4c1e1e9e4f05c07))

### Chores

- Add Issue Templates ([#17](https://github.com/Twingate/kubernetes-operator/pull/17),
  [`b478434`](https://github.com/Twingate/kubernetes-operator/commit/b47843494d2e3e4549cad10d9814fead08a43353))

- Bump black from 23.10.0 to 23.10.1
  ([#12](https://github.com/Twingate/kubernetes-operator/pull/12),
  [`1c8d684`](https://github.com/Twingate/kubernetes-operator/commit/1c8d6846b9ad1574c13d6541aeb0113040206767))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <205185+ekampf@users.noreply.github.com>

- Bump orjson from 3.9.9 to 3.9.10 ([#9](https://github.com/Twingate/kubernetes-operator/pull/9),
  [`298cccb`](https://github.com/Twingate/kubernetes-operator/commit/298cccbfa866ac39d090a77f1524d7aedd8e1e1d))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump pytest from 7.4.2 to 7.4.3 ([#7](https://github.com/Twingate/kubernetes-operator/pull/7),
  [`089ce2b`](https://github.com/Twingate/kubernetes-operator/commit/089ce2b6ae94a710e65d8af1d6d9aeb9951f7ec7))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump python-semantic-release from 8.1.2 to 8.3.0
  ([#10](https://github.com/Twingate/kubernetes-operator/pull/10),
  [`70b3a0c`](https://github.com/Twingate/kubernetes-operator/commit/70b3a0c18a2a752111026c0c8d58cca0b0a0fc97))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- Bump ruff from 0.1.1 to 0.1.3 ([#8](https://github.com/Twingate/kubernetes-operator/pull/8),
  [`e1524de`](https://github.com/Twingate/kubernetes-operator/commit/e1524de8dbdbc6f8f305b21c63da08cc632f3b72))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

Co-authored-by: Eran Kampf <205185+ekampf@users.noreply.github.com>

- Bump syrupy from 4.5.0 to 4.6.0 ([#11](https://github.com/Twingate/kubernetes-operator/pull/11),
  [`5e5b1f0`](https://github.com/Twingate/kubernetes-operator/commit/5e5b1f0ff55f4546a08d50742088afb4c498d543))

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Documentation

- Readme overhaul ([#15](https://github.com/Twingate/kubernetes-operator/pull/15),
  [`3c8e29c`](https://github.com/Twingate/kubernetes-operator/commit/3c8e29c309b2b5f6a7621db3e8842f703d5fb83e))

### Features

- Initial operator ([#1](https://github.com/Twingate/kubernetes-operator/pull/1),
  [`0bc53a8`](https://github.com/Twingate/kubernetes-operator/commit/0bc53a8ae9f3ed39486adbf7f57b4bf3774aff87))

- Support protocol restrictions on twingateresource
  ([#16](https://github.com/Twingate/kubernetes-operator/pull/16),
  [`0c95107`](https://github.com/Twingate/kubernetes-operator/commit/0c95107414e14d1624caf1e30b1acf5335a2a01c))


## v0.0.1 (2023-10-20)
