# CHANGELOG


## v0.25.1 (2025-07-17)

### Chores

- Bump aiohttp from 3.10.11 to 3.12.14
  ([#721](https://github.com/Twingate/kubernetes-operator/pull/721),
  [`9f33fa6`](https://github.com/Twingate/kubernetes-operator/commit/9f33fa6dd815f11414151dc6507fd11a4f5ca044))

- Bump kubernetes-access-gateway from 0.6.0 to 0.7.0 in /deploy/twingate-operator
  ([#725](https://github.com/Twingate/kubernetes-operator/pull/725),
  [`71e5259`](https://github.com/Twingate/kubernetes-operator/commit/71e5259963c686d3b28f9ef195c7663940fcefe7))

- Bump mypy from 1.16.1 to 1.17.0 ([#722](https://github.com/Twingate/kubernetes-operator/pull/722),
  [`18229bb`](https://github.com/Twingate/kubernetes-operator/commit/18229bb3851d52863ca8917479c99192299ef8ea))

- Bump orjson from 3.10.18 to 3.11.0
  ([#723](https://github.com/Twingate/kubernetes-operator/pull/723),
  [`393d410`](https://github.com/Twingate/kubernetes-operator/commit/393d410fd3b7f828c26979cc001446725e141d27))

- Bump ruff from 0.12.2 to 0.12.3 ([#720](https://github.com/Twingate/kubernetes-operator/pull/720),
  [`7bfe88b`](https://github.com/Twingate/kubernetes-operator/commit/7bfe88bd0ed6f25c7630a9a58af53d562195d6dd))


## v0.25.0 (2025-07-09)

### Chores

- Bump bandit from 1.8.5 to 1.8.6 ([#715](https://github.com/Twingate/kubernetes-operator/pull/715),
  [`b6a9a45`](https://github.com/Twingate/kubernetes-operator/commit/b6a9a45398aa46388ed89ac5083cd418122f51a9))

- Bump cryptography from 45.0.4 to 45.0.5
  ([#712](https://github.com/Twingate/kubernetes-operator/pull/712),
  [`520b72c`](https://github.com/Twingate/kubernetes-operator/commit/520b72c4c5bbd5f192bb67561698b83a5618c01a))

- Bump kubernetes-access-gateway from 0.5.1 to 0.6.0 in /deploy/twingate-operator
  ([#716](https://github.com/Twingate/kubernetes-operator/pull/716),
  [`8cd749a`](https://github.com/Twingate/kubernetes-operator/commit/8cd749a4e45c668ede4eb13f865e7f35b4d2bf2b))

- Bump pytest-factoryboy from 2.7.0 to 2.8.0
  ([#709](https://github.com/Twingate/kubernetes-operator/pull/709),
  [`8711110`](https://github.com/Twingate/kubernetes-operator/commit/87111101f541ce35a2df1ac8a745b1e171e22b7c))

- Bump pytest-factoryboy from 2.8.0 to 2.8.1
  ([#711](https://github.com/Twingate/kubernetes-operator/pull/711),
  [`62714ce`](https://github.com/Twingate/kubernetes-operator/commit/62714ce0e6003140614a47440fbd5eead0f6d9c9))

- Bump ruff from 0.12.1 to 0.12.2 ([#713](https://github.com/Twingate/kubernetes-operator/pull/713),
  [`61e0655`](https://github.com/Twingate/kubernetes-operator/commit/61e065533c23993afd4ead5b05b4bc9914900244))

### Features

- Add `nodeSelector`, `tolerations` and `affinity` to `pre-delete-cleanup` job template
  ([#714](https://github.com/Twingate/kubernetes-operator/pull/714),
  [`e6ce90b`](https://github.com/Twingate/kubernetes-operator/commit/e6ce90b01e78c3312b3f63aa35b7cff02e3c6217))

- Delete Kubernetes Access Gateway k8s Service object before removing operator
  ([#710](https://github.com/Twingate/kubernetes-operator/pull/710),
  [`2d89df1`](https://github.com/Twingate/kubernetes-operator/commit/2d89df10c110e396ff44bb02a8a7b58abaabc0b9))


## v0.24.0 (2025-06-30)

### Chores

- Bump ncipollo/release-action from 1.16.0 to 1.18.0
  ([#707](https://github.com/Twingate/kubernetes-operator/pull/707),
  [`4a95181`](https://github.com/Twingate/kubernetes-operator/commit/4a95181e6f73f8ecff427b329295d63284a9178f))

- Bump python-semantic-release from 10.1.0 to 10.2.0
  ([#708](https://github.com/Twingate/kubernetes-operator/pull/708),
  [`225e022`](https://github.com/Twingate/kubernetes-operator/commit/225e022ef21544ca310f318e9d45cae1bb4365bc))

- Bump ruff from 0.12.0 to 0.12.1 ([#705](https://github.com/Twingate/kubernetes-operator/pull/705),
  [`2fe6d32`](https://github.com/Twingate/kubernetes-operator/commit/2fe6d32710a88b3d918df0fa4ffcaa8fead78b36))

- Update asdf to Python 3.12.11
  ([`5090d12`](https://github.com/Twingate/kubernetes-operator/commit/5090d12b78a4a6e93a4f796152b8f9715cb53284))

### Features

- Create aggregate cluster roles ([#706](https://github.com/Twingate/kubernetes-operator/pull/706),
  [`f9dfca0`](https://github.com/Twingate/kubernetes-operator/commit/f9dfca00adb857e83677a2ac8a2b546e7202fc64))

- Improve validation - ‘spec’ is always required
  ([#704](https://github.com/Twingate/kubernetes-operator/pull/704),
  [`be00936`](https://github.com/Twingate/kubernetes-operator/commit/be009365012285fa7ab7541d79777909d5a0dff1))


## v0.23.1 (2025-06-26)

### Chores

- Bump kubernetes-access-gateway from 0.5.0 to 0.5.1 in /deploy/twingate-operator
  ([#702](https://github.com/Twingate/kubernetes-operator/pull/702),
  [`8c65a10`](https://github.com/Twingate/kubernetes-operator/commit/8c65a10e0003a7024588c90824126ee40cfd81ab))

- Bump types-croniter from 6.0.0.20250411 to 6.0.0.20250626
  ([#703](https://github.com/Twingate/kubernetes-operator/pull/703),
  [`f8f4aa5`](https://github.com/Twingate/kubernetes-operator/commit/f8f4aa54d59dcfdd38fc6b200923bfb8cf4fa8b7))

- Fix CHANGELOG generation folowing python-semantic-release v10 change
  ([`1cad486`](https://github.com/Twingate/kubernetes-operator/commit/1cad486f0a1388114e9da69c5ea82bc8797c551d))

### Documentation

- README update
  ([`ce0d69a`](https://github.com/Twingate/kubernetes-operator/commit/ce0d69a570017ff23fa15a4a73c38afe9ccd9b71))

- Update changelog for v0.23.0
  ([`31eab1c`](https://github.com/Twingate/kubernetes-operator/commit/31eab1c040556086d3b351a9973fe516035e15bb))


## v0.23.0 (2025-06-24)

### Bug Fixes

- Allow_zero_version should be true
  ([#664](https://github.com/Twingate/kubernetes-operator/pull/664),
  [`b174ec9`](https://github.com/Twingate/kubernetes-operator/commit/b174ec91da9969d421e370b26aaf58923686aa3d))

- Always use `kubernetes.default.svc.cluster.local` as the address of a k8s resource
  ([#670](https://github.com/Twingate/kubernetes-operator/pull/670),
  [`d122c09`](https://github.com/Twingate/kubernetes-operator/commit/d122c09a07fc145418f53b0d81cadc579b4d1c20))

- Can’t patch status of Service objects
  ([#685](https://github.com/Twingate/kubernetes-operator/pull/685),
  [`d94c820`](https://github.com/Twingate/kubernetes-operator/commit/d94c820a1ccc66b91f5639da26ce100ee34a3c74))

- Get resource should only return None if not found
  ([#662](https://github.com/Twingate/kubernetes-operator/pull/662),
  [`6cea8b0`](https://github.com/Twingate/kubernetes-operator/commit/6cea8b02b5ab1685c51a8454b0a5936df5b20c43))

- Only call resource update when spec\labels update
  ([#681](https://github.com/Twingate/kubernetes-operator/pull/681),
  [`86efe82`](https://github.com/Twingate/kubernetes-operator/commit/86efe82b48b326b28fa492322c673e8ed5794663))

- Pod to Deployment migration doesnt work with imagePolicy
  ([#674](https://github.com/Twingate/kubernetes-operator/pull/674),
  [`59d57d7`](https://github.com/Twingate/kubernetes-operator/commit/59d57d7a100756b951a193a36a83bec7446cff88))

### Chores

- Bump bandit from 1.8.3 to 1.8.5 ([#694](https://github.com/Twingate/kubernetes-operator/pull/694),
  [`ac8ec19`](https://github.com/Twingate/kubernetes-operator/commit/ac8ec19a826e7488462914b9a759700251142b4e))

- Bump cryptography from 44.0.2 to 45.0.2
  ([#659](https://github.com/Twingate/kubernetes-operator/pull/659),
  [`57ad6f5`](https://github.com/Twingate/kubernetes-operator/commit/57ad6f5314a1e21cb4650a4d7e80f43177948825))

- Bump cryptography from 45.0.2 to 45.0.3
  ([#660](https://github.com/Twingate/kubernetes-operator/pull/660),
  [`b3c254e`](https://github.com/Twingate/kubernetes-operator/commit/b3c254e0d8c8959154e3e6d523bf61f2151fd190))

- Bump cryptography from 45.0.3 to 45.0.4
  ([#679](https://github.com/Twingate/kubernetes-operator/pull/679),
  [`2521d14`](https://github.com/Twingate/kubernetes-operator/commit/2521d147dbf827e19c373f72070599fe2959b447))

- Bump github.com/gruntwork-io/terratest from 0.49.0 to 0.50.0
  ([#692](https://github.com/Twingate/kubernetes-operator/pull/692),
  [`ba4635c`](https://github.com/Twingate/kubernetes-operator/commit/ba4635cac48f12e655eb952e487e92843daa9803))

- Bump google-cloud-artifact-registry from 1.16.0 to 1.16.1
  ([#682](https://github.com/Twingate/kubernetes-operator/pull/682),
  [`58feda2`](https://github.com/Twingate/kubernetes-operator/commit/58feda209e1e3945f7dde692beb72ef61384ffbb))

- Bump kubernetes from 32.0.1 to 33.1.0
  ([#686](https://github.com/Twingate/kubernetes-operator/pull/686),
  [`a2cc02d`](https://github.com/Twingate/kubernetes-operator/commit/a2cc02dd3c2a1d1dcd257de5100701c01a20dee4))

- Bump kubernetes-access-gateway from 0.1.2 to 0.2.1 in /deploy/twingate-operator
  ([#675](https://github.com/Twingate/kubernetes-operator/pull/675),
  [`08832ad`](https://github.com/Twingate/kubernetes-operator/commit/08832ad623beec76b7b123fcad723dea595ba228))

- Bump kubernetes-access-gateway from 0.2.1 to 0.4.0 in /deploy/twingate-operator
  ([#688](https://github.com/Twingate/kubernetes-operator/pull/688),
  [`97f1a87`](https://github.com/Twingate/kubernetes-operator/commit/97f1a879b6095ebe35561a280e073e622b2f0dad))

- Bump kubernetes-access-gateway from 0.4.0 to 0.5.0 in /deploy/twingate-operator
  ([#701](https://github.com/Twingate/kubernetes-operator/pull/701),
  [`f8e31ee`](https://github.com/Twingate/kubernetes-operator/commit/f8e31ee93ad5d04f81ba5940160c0cb3d8d5763b))

- Bump mypy from 1.15.0 to 1.16.0 ([#666](https://github.com/Twingate/kubernetes-operator/pull/666),
  [`57bf107`](https://github.com/Twingate/kubernetes-operator/commit/57bf10768a6faa9272ff2ccb03c57ae2b0f7cfc3))

- Bump mypy from 1.16.0 to 1.16.1 ([#695](https://github.com/Twingate/kubernetes-operator/pull/695),
  [`1f1cb5e`](https://github.com/Twingate/kubernetes-operator/commit/1f1cb5eda19ee97932320ab113d063440de14004))

- Bump protobuf from 4.25.1 to 4.25.8
  ([#693](https://github.com/Twingate/kubernetes-operator/pull/693),
  [`1eea1a3`](https://github.com/Twingate/kubernetes-operator/commit/1eea1a38026dba7765d2115c966c5ee5b444b945))

- Bump pydantic from 2.11.5 to 2.11.6
  ([#687](https://github.com/Twingate/kubernetes-operator/pull/687),
  [`64cfd7c`](https://github.com/Twingate/kubernetes-operator/commit/64cfd7c1494c5c9b67e10042dcba8d52d4b5d57d))

- Bump pydantic from 2.11.6 to 2.11.7
  ([#691](https://github.com/Twingate/kubernetes-operator/pull/691),
  [`ecdfd88`](https://github.com/Twingate/kubernetes-operator/commit/ecdfd883863264fc899c9227e5e7cda6ebb9a43e))

- Bump pydantic-settings from 2.10.0 to 2.10.1
  ([#700](https://github.com/Twingate/kubernetes-operator/pull/700),
  [`44e9645`](https://github.com/Twingate/kubernetes-operator/commit/44e9645bc3b066a8603bd0726aeba1227b5a29a5))

- Bump pydantic-settings from 2.9.1 to 2.10.0
  ([#699](https://github.com/Twingate/kubernetes-operator/pull/699),
  [`9a039dd`](https://github.com/Twingate/kubernetes-operator/commit/9a039dd473f08675cacdc7abee25632ed37c2b58))

- Bump pytest-cov from 6.1.1 to 6.2.1
  ([#684](https://github.com/Twingate/kubernetes-operator/pull/684),
  [`31978f8`](https://github.com/Twingate/kubernetes-operator/commit/31978f8107436a7d4a692fe8252e618a17493f93))

- Bump pytest-datadir from 1.6.1 to 1.7.0
  ([#667](https://github.com/Twingate/kubernetes-operator/pull/667),
  [`38caa51`](https://github.com/Twingate/kubernetes-operator/commit/38caa5178374ac6a28f933a4ba7d447c85609c87))

- Bump pytest-datadir from 1.7.0 to 1.7.1
  ([#672](https://github.com/Twingate/kubernetes-operator/pull/672),
  [`4e317b8`](https://github.com/Twingate/kubernetes-operator/commit/4e317b807deebe35440c40ea651df7b6aacd04dc))

- Bump pytest-datadir from 1.7.1 to 1.7.2
  ([#677](https://github.com/Twingate/kubernetes-operator/pull/677),
  [`02d1446`](https://github.com/Twingate/kubernetes-operator/commit/02d14465245a0fdebecd1f90ed3703f4a16e0a65))

- Bump python-semantic-release from 10.0.2 to 10.1.0
  ([#683](https://github.com/Twingate/kubernetes-operator/pull/683),
  [`c82efa3`](https://github.com/Twingate/kubernetes-operator/commit/c82efa345a22cf53684def1b8796639bcad193ec))

- Bump python-semantic-release from 9.21.1 to 10.0.2
  ([#661](https://github.com/Twingate/kubernetes-operator/pull/661),
  [`ec84182`](https://github.com/Twingate/kubernetes-operator/commit/ec84182cc49e6a88109564b78a98495be04998ab))

- Bump pyupgrade from 3.19.1 to 3.20.0
  ([#658](https://github.com/Twingate/kubernetes-operator/pull/658),
  [`8a2d61c`](https://github.com/Twingate/kubernetes-operator/commit/8a2d61c40906a8e9b38c450542ee863a47ab2cea))

- Bump requests from 2.32.3 to 2.32.4
  ([#678](https://github.com/Twingate/kubernetes-operator/pull/678),
  [`6efe0f8`](https://github.com/Twingate/kubernetes-operator/commit/6efe0f87b8a9a08123b20a5fb5bc567352ac19c1))

- Bump ruff from 0.11.11 to 0.11.12
  ([#665](https://github.com/Twingate/kubernetes-operator/pull/665),
  [`bfb991c`](https://github.com/Twingate/kubernetes-operator/commit/bfb991c9c4a4faaa426df1add90b9ec4e7ac6ae4))

- Bump ruff from 0.11.12 to 0.11.13
  ([#676](https://github.com/Twingate/kubernetes-operator/pull/676),
  [`27e60df`](https://github.com/Twingate/kubernetes-operator/commit/27e60dfa8157c965003366a6de6c246ec83b43cd))

- Bump ruff from 0.11.13 to 0.12.0
  ([#696](https://github.com/Twingate/kubernetes-operator/pull/696),
  [`db53f47`](https://github.com/Twingate/kubernetes-operator/commit/db53f47566208dd1d72fab8f6cf322651c5283b1))

- Bump types-requests from 2.32.0.20250515 to 2.32.0.20250602
  ([#669](https://github.com/Twingate/kubernetes-operator/pull/669),
  [`0f00684`](https://github.com/Twingate/kubernetes-operator/commit/0f00684026846146654f526905b85d262c901c66))

- Bump types-requests from 2.32.0.20250602 to 2.32.4.20250611
  ([#680](https://github.com/Twingate/kubernetes-operator/pull/680),
  [`c2812a1`](https://github.com/Twingate/kubernetes-operator/commit/c2812a1be08f4919bd7e78bb7ff37701f47d1bde))

- Bump urllib3 from 2.2.2 to 2.5.0
  ([#698](https://github.com/Twingate/kubernetes-operator/pull/698),
  [`f0ce1b3`](https://github.com/Twingate/kubernetes-operator/commit/f0ce1b357bfbbd96cfec022beac96b41d4d2e501))

- Fix dependabot.yml
  ([`e59a0da`](https://github.com/Twingate/kubernetes-operator/commit/e59a0da6a7f084660fcba24bad9559d6f7666ba7))

- Ignore pre-releases in helm dependabot
  ([`2d8e808`](https://github.com/Twingate/kubernetes-operator/commit/2d8e808f24f82a853440678953b6f8e4134b1756))

- Release dev helm chart OCI when pushing to `main`
  ([#663](https://github.com/Twingate/kubernetes-operator/pull/663),
  [`cfebfd7`](https://github.com/Twingate/kubernetes-operator/commit/cfebfd7aea0853e5b9bf4777a8ec37f61508e5aa))

### Documentation

- Added README note regarding CRD updates
  ([`14563a8`](https://github.com/Twingate/kubernetes-operator/commit/14563a8f1616f81e9a1f632b9d3da3f969fc5dcd))

### Features

- Support creating `LoadBalancer` Service type for Kubernetes Resource
  ([#668](https://github.com/Twingate/kubernetes-operator/pull/668),
  [`c231b4d`](https://github.com/Twingate/kubernetes-operator/commit/c231b4d6c37a22604722d617535f25f4d411a02f))

- Support for Twingate Kubernetes Access Gateway
  ([#648](https://github.com/Twingate/kubernetes-operator/pull/648),
  [`9c4cc0a`](https://github.com/Twingate/kubernetes-operator/commit/9c4cc0a6318f05a92f015134bfb07e49f0fbd15a))

- Support using `LoadBalancer` service hostname as proxy address
  ([#690](https://github.com/Twingate/kubernetes-operator/pull/690),
  [`1b76b4e`](https://github.com/Twingate/kubernetes-operator/commit/1b76b4ed0d587c919ed5b5458b4bcd379593a2b1))


## v0.22.1 (2025-05-23)

### Bug Fixes

- Dont use a well known label name as selector
  ([#653](https://github.com/Twingate/kubernetes-operator/pull/653),
  [`e02ff51`](https://github.com/Twingate/kubernetes-operator/commit/e02ff51979de8455e197173f19ddc5c6160d5b9b))

- Reconciler should only update k8s if there’s drift in image
  ([#654](https://github.com/Twingate/kubernetes-operator/pull/654),
  [`5ad0e3e`](https://github.com/Twingate/kubernetes-operator/commit/5ad0e3e95fd8296ba924e949a14f704d75774594))

### Chores

- Bump gql from 3.5.2 to 3.5.3 ([#650](https://github.com/Twingate/kubernetes-operator/pull/650),
  [`9d76ffa`](https://github.com/Twingate/kubernetes-operator/commit/9d76ffabf79977b1e795ab1719528eef7b4302f0))

- Bump pydantic from 2.11.4 to 2.11.5
  ([#655](https://github.com/Twingate/kubernetes-operator/pull/655),
  [`38d637b`](https://github.com/Twingate/kubernetes-operator/commit/38d637b100a28971b484d6f0d3bae91b3380b6fd))

- Bump ruff from 0.11.10 to 0.11.11
  ([#656](https://github.com/Twingate/kubernetes-operator/pull/656),
  [`d4075cf`](https://github.com/Twingate/kubernetes-operator/commit/d4075cf4061c8c1cf1da4e266d87404757d37272))

- Bump setuptools from 70.0.0 to 78.1.1
  ([#647](https://github.com/Twingate/kubernetes-operator/pull/647),
  [`b60464b`](https://github.com/Twingate/kubernetes-operator/commit/b60464be9cedbcee2dbddb0777274e28aecfbc11))

### Documentation

- Operator no longer beta!
  ([`3a9efaf`](https://github.com/Twingate/kubernetes-operator/commit/3a9efaf22cdb719ed8825e1ae9f21e5ce5753675))


## v0.22.0 (2025-05-19)

### Bug Fixes

- Add client_timeout setting to prevent operator disconnect
  ([#646](https://github.com/Twingate/kubernetes-operator/pull/646),
  [`53f911d`](https://github.com/Twingate/kubernetes-operator/commit/53f911d010e094df70b4826383412ecf787579be))

### Chores

- Bump ruff from 0.11.9 to 0.11.10
  ([#645](https://github.com/Twingate/kubernetes-operator/pull/645),
  [`45f54ed`](https://github.com/Twingate/kubernetes-operator/commit/45f54edfecda369610677da3b2f4b2b876c0c449))

- Bump types-pyyaml from 6.0.12.20250402 to 6.0.12.20250516
  ([#644](https://github.com/Twingate/kubernetes-operator/pull/644),
  [`592ad39`](https://github.com/Twingate/kubernetes-operator/commit/592ad39f25e20ea8c8760517c4a9854c8b735738))

- Bump types-requests from 2.32.0.20250328 to 2.32.0.20250515
  ([#643](https://github.com/Twingate/kubernetes-operator/pull/643),
  [`924ecae`](https://github.com/Twingate/kubernetes-operator/commit/924ecaef9c2708b2c5b132b4c3586cc0571fe436))

### Features

- Change TwingateConnector to use Deployment or Pod
  ([#633](https://github.com/Twingate/kubernetes-operator/pull/633),
  [`6d342a7`](https://github.com/Twingate/kubernetes-operator/commit/6d342a725bc85ac4251d45afa5a3f84be5837c81))


## v0.21.2 (2025-05-13)

### Bug Fixes

- Add permissions for deployments required to run connectors
  ([`d187a1a`](https://github.com/Twingate/kubernetes-operator/commit/d187a1ab6ba2b0615db22d1a31a325399c7ad23b))

### Chores

- Bump github.com/gruntwork-io/terratest from 0.48.2 to 0.49.0
  ([#637](https://github.com/Twingate/kubernetes-operator/pull/637),
  [`1fc33cf`](https://github.com/Twingate/kubernetes-operator/commit/1fc33cf90841266bbe3f4f0c13aa68cf805776e8))

- Bump kopf from 1.37.5 to 1.38.0 ([#639](https://github.com/Twingate/kubernetes-operator/pull/639),
  [`c5aab19`](https://github.com/Twingate/kubernetes-operator/commit/c5aab1948f6c0a01e6967412dd5bbdb8ac187572))

- Bump ruff from 0.11.8 to 0.11.9 ([#638](https://github.com/Twingate/kubernetes-operator/pull/638),
  [`4d61918`](https://github.com/Twingate/kubernetes-operator/commit/4d61918dc1452236f9e1e5e0cb23e60c885c4909))

- Update certifi package version to 2025.4.26 for improved security and compatibility
  ([`a6e0e37`](https://github.com/Twingate/kubernetes-operator/commit/a6e0e37751f7348b21f45f041f1724d337a33884))

- Update pytz package version from 2023.3.post1 to 2025.2 to ensure compatibility and access to the
  latest features and fixes
  ([`a1c6fdc`](https://github.com/Twingate/kubernetes-operator/commit/a1c6fdcb81ae9627dccc1f85172d42c6079ae938))

### Testing

- Remove unused `pytest-freezegun` library
  ([#640](https://github.com/Twingate/kubernetes-operator/pull/640),
  [`5f08dda`](https://github.com/Twingate/kubernetes-operator/commit/5f08dda0f638b2d36e960ee56003fef2c2fd22e4))


## v0.21.1 (2025-05-08)

### Bug Fixes

- Update operator ClusterRole permissions for twingate.com apiGroup
  ([#636](https://github.com/Twingate/kubernetes-operator/pull/636),
  [`dae0916`](https://github.com/Twingate/kubernetes-operator/commit/dae0916092dc677ee49112a9cc13a515298861de))


## v0.21.0 (2025-05-07)

### Bug Fixes

- Add delete permission to Twingate resources
  ([#634](https://github.com/Twingate/kubernetes-operator/pull/634),
  [`dd6b242`](https://github.com/Twingate/kubernetes-operator/commit/dd6b242df0281d51347057a1cc1e1345969753ea))

### Chores

- Bump python-semantic-release from 9.21.0 to 9.21.1
  ([#632](https://github.com/Twingate/kubernetes-operator/pull/632),
  [`1446548`](https://github.com/Twingate/kubernetes-operator/commit/14465483d3c5a46b1846b982079ece9923e64c83))

- Bump ruff from 0.11.7 to 0.11.8 ([#630](https://github.com/Twingate/kubernetes-operator/pull/630),
  [`20ae013`](https://github.com/Twingate/kubernetes-operator/commit/20ae0137c24fd0d9b6f6ad3c5d6866b95f2000a7))

- Nicer Makefile
  ([`f67790b`](https://github.com/Twingate/kubernetes-operator/commit/f67790b8119cd222fd4516a6e7029c751e0ad84a))

- Update asdf to Python 3.12.10
  ([`7c9e2a4`](https://github.com/Twingate/kubernetes-operator/commit/7c9e2a424abc5f0e8c97a8af57d5cbd9f4dc1e7d))

- Update coveralls dependency ([#635](https://github.com/Twingate/kubernetes-operator/pull/635),
  [`a21e955`](https://github.com/Twingate/kubernetes-operator/commit/a21e955571eeb2aed5ad3df118b95054a0d79520))

### Features

- Add default value for repository source to streamline configuration process
  ([#631](https://github.com/Twingate/kubernetes-operator/pull/631),
  [`7cbcd7f`](https://github.com/Twingate/kubernetes-operator/commit/7cbcd7f6356f4562ca867fa8dcec6fc488c2b606))


## v0.20.2 (2025-04-30)

### Bug Fixes

- Operator should halt if settings are invalid
  ([#623](https://github.com/Twingate/kubernetes-operator/pull/623),
  [`2d0f1c3`](https://github.com/Twingate/kubernetes-operator/commit/2d0f1c34204070906d2aeb03f7fd2bd681ddf8fa))

- Skip `twingate_resource_update` handler when `spec.id` is added
  ([#627](https://github.com/Twingate/kubernetes-operator/pull/627),
  [`aeb3758`](https://github.com/Twingate/kubernetes-operator/commit/aeb37583d9e395c271c67661e9ba56a311ea17ed))

### Chores

- Bump orjson from 3.10.16 to 3.10.18
  ([#628](https://github.com/Twingate/kubernetes-operator/pull/628),
  [`2c12e5d`](https://github.com/Twingate/kubernetes-operator/commit/2c12e5d606671f7de921cc476febd5cd51e686c3))

- Bump pendulum from 3.0.0 to 3.1.0
  ([#625](https://github.com/Twingate/kubernetes-operator/pull/625),
  [`cc5c276`](https://github.com/Twingate/kubernetes-operator/commit/cc5c2762696e2d503a6e04cb88e7e57dd80fc541))

- Bump pydantic from 2.11.3 to 2.11.4
  ([#629](https://github.com/Twingate/kubernetes-operator/pull/629),
  [`542ef8c`](https://github.com/Twingate/kubernetes-operator/commit/542ef8c18504fb068e44126b9b73315db0186190))

- Bump pydantic-settings from 2.9.0 to 2.9.1
  ([#624](https://github.com/Twingate/kubernetes-operator/pull/624),
  [`9cd8168`](https://github.com/Twingate/kubernetes-operator/commit/9cd8168fac83f2981347b50ea4e044681b8d118a))

- Bump ruff from 0.11.6 to 0.11.7 ([#626](https://github.com/Twingate/kubernetes-operator/pull/626),
  [`e4d7b61`](https://github.com/Twingate/kubernetes-operator/commit/e4d7b617d79b254c8af3669faeae95d1fd27962d))

- Removed duplicate “RSE” ruff rule and added “UP”
  ([`3e7d29c`](https://github.com/Twingate/kubernetes-operator/commit/3e7d29c4993df6d536b1fa52b83dcc5cf9f93d69))


## v0.20.1 (2025-04-18)

### Bug Fixes

- TWINGATE_DEFAULT_RESOURCE_TAGS default value should be empty dict
  ([#622](https://github.com/Twingate/kubernetes-operator/pull/622),
  [`29a1679`](https://github.com/Twingate/kubernetes-operator/commit/29a1679d9318a1a5869bce29380214097603b1eb))

### Chores

- Bump golang.org/x/net from 0.36.0 to 0.38.0
  ([#618](https://github.com/Twingate/kubernetes-operator/pull/618),
  [`0125265`](https://github.com/Twingate/kubernetes-operator/commit/01252655333c2f1bad80129947f6b8ad5102845f))

- Bump pydantic-settings from 2.8.1 to 2.9.0
  ([#620](https://github.com/Twingate/kubernetes-operator/pull/620),
  [`29f4573`](https://github.com/Twingate/kubernetes-operator/commit/29f45737d823480585c23662b9079ecb9557993e))

- Bump ruff from 0.11.5 to 0.11.6 ([#621](https://github.com/Twingate/kubernetes-operator/pull/621),
  [`4dd320d`](https://github.com/Twingate/kubernetes-operator/commit/4dd320d88af14c0730274881b0cc75cfc812fb4a))

### Testing

- Improve tests for `get_connector_pod()` and `test_handler_resources`
  ([#619](https://github.com/Twingate/kubernetes-operator/pull/619),
  [`3322937`](https://github.com/Twingate/kubernetes-operator/commit/3322937ea0d67cd8235240a439ab5de2d09c4c8d))


## v0.20.0 (2025-04-16)

### Bug Fixes

- `defaultResourceTags` to match labels schema
  ([#617](https://github.com/Twingate/kubernetes-operator/pull/617),
  [`f0fd5cc`](https://github.com/Twingate/kubernetes-operator/commit/f0fd5ccb6aaf48b9d9018a9a1f3fd5a9a02e12f7))

- K8s Service annotations not removed properly
  ([#610](https://github.com/Twingate/kubernetes-operator/pull/610),
  [`1e2b7ae`](https://github.com/Twingate/kubernetes-operator/commit/1e2b7ae7f1c6ea881d992b965e00c30dc2bb9eb1))

### Chores

- Bump danger/danger-js from 12.3.4 to 13.0.4
  ([#616](https://github.com/Twingate/kubernetes-operator/pull/616),
  [`216d644`](https://github.com/Twingate/kubernetes-operator/commit/216d644c732cd823001af5dc443ef5fc3d505035))

- Bump google-cloud-artifact-registry from 1.15.2 to 1.16.0
  ([#611](https://github.com/Twingate/kubernetes-operator/pull/611),
  [`6646803`](https://github.com/Twingate/kubernetes-operator/commit/66468039b764222f51a5de2b0fcc9f517326b403))

- Bump ruff from 0.11.4 to 0.11.5 ([#608](https://github.com/Twingate/kubernetes-operator/pull/608),
  [`bf3c26d`](https://github.com/Twingate/kubernetes-operator/commit/bf3c26df8733bbc6b4e08fa51ab1b772a784f43c))

- Bump types-croniter from 5.0.1.20250322 to 6.0.0.20250411
  ([#609](https://github.com/Twingate/kubernetes-operator/pull/609),
  [`862942d`](https://github.com/Twingate/kubernetes-operator/commit/862942d75d23be05fd00c5854c1beda45dfa08bc))

- Update `poetry install —sync` command to `poetry sync` as —sync is deprecated
  ([`8ba8561`](https://github.com/Twingate/kubernetes-operator/commit/8ba8561c381ac78602df4bec2b27dd7720388804))

### Documentation

- Improve `DEVELOPER.md` and `README.md` documentations
  ([#601](https://github.com/Twingate/kubernetes-operator/pull/601),
  [`81387a9`](https://github.com/Twingate/kubernetes-operator/commit/81387a982ca4d2f11e4f42c6954cbc41b90cfde9))

### Features

- Support `livenessProbe`, `readinessProbe` and enhance security by setting `readOnlyRootFilesystem`
  on `TwingateConnector` ([#612](https://github.com/Twingate/kubernetes-operator/pull/612),
  [`26bf5e1`](https://github.com/Twingate/kubernetes-operator/commit/26bf5e10703b76a8274d497593428c85b737c704))

- Support `syncLabels` on `TwingateResource.spec` and k8s `Service` annotations
  ([#606](https://github.com/Twingate/kubernetes-operator/pull/606),
  [`f9371b5`](https://github.com/Twingate/kubernetes-operator/commit/f9371b50f5196ee99d2f584c9c671e77bddf8b59))

- Support Twingate Resource tagging
  ([#605](https://github.com/Twingate/kubernetes-operator/pull/605),
  [`e77773d`](https://github.com/Twingate/kubernetes-operator/commit/e77773d38246bd1352bf6dd6af6271a50d8d13da))

- Supporting adding default tags on Twingate Resource
  ([#613](https://github.com/Twingate/kubernetes-operator/pull/613),
  [`a623091`](https://github.com/Twingate/kubernetes-operator/commit/a623091f3724698d9f6193a38342fac89f5690c9))


## v0.19.0 (2025-04-08)

### Bug Fixes

- **main.py**: Set server_timeout to 5 minutes to resolve change detection issue
  ([#599](https://github.com/Twingate/kubernetes-operator/pull/599),
  [`7001478`](https://github.com/Twingate/kubernetes-operator/commit/7001478cd14fddfe79acd7399c28c4e96ca56131))

### Chores

- Bump pydantic from 2.10.6 to 2.11.1
  ([#591](https://github.com/Twingate/kubernetes-operator/pull/591),
  [`4c432b2`](https://github.com/Twingate/kubernetes-operator/commit/4c432b2450db6d7007e279e3c413e70b81a0c055))

- Bump pydantic from 2.11.1 to 2.11.2
  ([#597](https://github.com/Twingate/kubernetes-operator/pull/597),
  [`c9a60e5`](https://github.com/Twingate/kubernetes-operator/commit/c9a60e5a7155ca4d4895fd958f31682d406b3c32))

- Bump pydantic from 2.11.2 to 2.11.3
  ([#602](https://github.com/Twingate/kubernetes-operator/pull/602),
  [`39f85d6`](https://github.com/Twingate/kubernetes-operator/commit/39f85d68955bc85afeda96fdcb5fee3b0cdd7209))

- Bump ruff from 0.11.2 to 0.11.3 ([#598](https://github.com/Twingate/kubernetes-operator/pull/598),
  [`0967e60`](https://github.com/Twingate/kubernetes-operator/commit/0967e604f5c0a85a1952712aa961d1934a094229))

- Bump ruff from 0.11.3 to 0.11.4 ([#600](https://github.com/Twingate/kubernetes-operator/pull/600),
  [`6aef5a5`](https://github.com/Twingate/kubernetes-operator/commit/6aef5a52e7626f6ba42cd7616b207ef6b136e404))

- Bump tenacity from 9.0.0 to 9.1.2
  ([#594](https://github.com/Twingate/kubernetes-operator/pull/594),
  [`c8fa1a1`](https://github.com/Twingate/kubernetes-operator/commit/c8fa1a1239a8e819ee3971b7917270b223d1f328))

- Bump types-pyyaml from 6.0.12.20250326 to 6.0.12.20250402
  ([#595](https://github.com/Twingate/kubernetes-operator/pull/595),
  [`bd8582e`](https://github.com/Twingate/kubernetes-operator/commit/bd8582e04c1b0080d1fb400f7185d5cbb7f5c8d5))

- Bump types-requests from 2.32.0.20250306 to 2.32.0.20250328
  ([#590](https://github.com/Twingate/kubernetes-operator/pull/590),
  [`ee88a8d`](https://github.com/Twingate/kubernetes-operator/commit/ee88a8d487ddba56fa2fd9f4d95842ce6f71503a))

- Remove redundant integration test marker
  ([#603](https://github.com/Twingate/kubernetes-operator/pull/603),
  [`bce6996`](https://github.com/Twingate/kubernetes-operator/commit/bce69966972c23cd0ea3bb1c4c02b03e45079c74))

### Features

- Improve logs for better debugging experience
  ([#592](https://github.com/Twingate/kubernetes-operator/pull/592),
  [`c6ec9e2`](https://github.com/Twingate/kubernetes-operator/commit/c6ec9e2d42fe03023a48d6e6cdc6cac041aeab7f))


## v0.18.0 (2025-03-26)

### Bug Fixes

- Support removing security policy from an access edge
  ([#583](https://github.com/Twingate/kubernetes-operator/pull/583),
  [`95a9932`](https://github.com/Twingate/kubernetes-operator/commit/95a99320db2f2470eb1ba8451f330aa7d93d7163))

### Chores

- Bump golang.org/x/net from 0.34.0 to 0.36.0
  ([#574](https://github.com/Twingate/kubernetes-operator/pull/574),
  [`540d508`](https://github.com/Twingate/kubernetes-operator/commit/540d508fc8230ee2d3e75cd12ad3691763137636))

- Bump google-cloud-artifact-registry from 1.15.1 to 1.15.2
  ([#577](https://github.com/Twingate/kubernetes-operator/pull/577),
  [`33738c7`](https://github.com/Twingate/kubernetes-operator/commit/33738c77b080b8d2470ca51e930579d307cbdb68))

- Bump gql from 3.5.1 to 3.5.2 ([#568](https://github.com/Twingate/kubernetes-operator/pull/568),
  [`d59d2c0`](https://github.com/Twingate/kubernetes-operator/commit/d59d2c0e2735823cf25e70e9b1c0fb56110aa414))

- Bump jinja2 from 3.1.5 to 3.1.6 ([#569](https://github.com/Twingate/kubernetes-operator/pull/569),
  [`4f40172`](https://github.com/Twingate/kubernetes-operator/commit/4f4017248d3994a1de8150a95258b8d66bc3787c))

- Bump kopf from 1.37.4 to 1.37.5 ([#586](https://github.com/Twingate/kubernetes-operator/pull/586),
  [`a827c42`](https://github.com/Twingate/kubernetes-operator/commit/a827c42c065918dcd0bd77b05d2df366801ab5a0))

- Bump multidict from 6.0.4 to 6.2.0
  ([`c2a23ef`](https://github.com/Twingate/kubernetes-operator/commit/c2a23efa65e91e4afd627a7bd62b795dca3c5d9d))

- Bump orjson from 3.10.15 to 3.10.16
  ([#587](https://github.com/Twingate/kubernetes-operator/pull/587),
  [`d4708cd`](https://github.com/Twingate/kubernetes-operator/commit/d4708cd1105fdc3d5164c2729a83d18e60c71369))

- Bump pre-commit from 4.1.0 to 4.2.0
  ([#580](https://github.com/Twingate/kubernetes-operator/pull/580),
  [`fba7e1d`](https://github.com/Twingate/kubernetes-operator/commit/fba7e1d59ecec5441b50d221afcb3a5f76c3b8a0))

- Bump pydantic-settings from 2.8.0 to 2.8.1
  ([#561](https://github.com/Twingate/kubernetes-operator/pull/561),
  [`03be561`](https://github.com/Twingate/kubernetes-operator/commit/03be56195b9dbbb0316ed74883426c6a4a253e61))

- Bump pytest from 8.3.4 to 8.3.5 ([#565](https://github.com/Twingate/kubernetes-operator/pull/565),
  [`a78e444`](https://github.com/Twingate/kubernetes-operator/commit/a78e444209aabf15b1123404a26754e3c21fe79e))

- Bump responses from 0.25.6 to 0.25.7
  ([#573](https://github.com/Twingate/kubernetes-operator/pull/573),
  [`6c68c1e`](https://github.com/Twingate/kubernetes-operator/commit/6c68c1ed78799e03bb004c1ed83ba844595be52f))

- Bump ruff from 0.10.0 to 0.11.0 ([#578](https://github.com/Twingate/kubernetes-operator/pull/578),
  [`5b618d3`](https://github.com/Twingate/kubernetes-operator/commit/5b618d3958d6caf33c79a4364e1f3faa5b0c9be2))

- Bump ruff from 0.11.0 to 0.11.2 ([#582](https://github.com/Twingate/kubernetes-operator/pull/582),
  [`3de31fe`](https://github.com/Twingate/kubernetes-operator/commit/3de31fee04bbcc579c37fccfd87f93e8f7ae9593))

- Bump ruff from 0.9.10 to 0.10.0 ([#576](https://github.com/Twingate/kubernetes-operator/pull/576),
  [`6cc42e7`](https://github.com/Twingate/kubernetes-operator/commit/6cc42e7d54c1df34e087fdf774d00858f2c22dbe))

- Bump ruff from 0.9.7 to 0.9.9 ([#566](https://github.com/Twingate/kubernetes-operator/pull/566),
  [`bcd9020`](https://github.com/Twingate/kubernetes-operator/commit/bcd9020308f09fda5d2e3a90c10bc7647d53b1dd))

- Bump ruff from 0.9.9 to 0.9.10 ([#571](https://github.com/Twingate/kubernetes-operator/pull/571),
  [`b030bf6`](https://github.com/Twingate/kubernetes-operator/commit/b030bf6dec1d3ea6c1cc6740b5c75c4e339ae9e3))

- Bump syrupy from 4.8.2 to 4.9.0 ([#572](https://github.com/Twingate/kubernetes-operator/pull/572),
  [`7933a9b`](https://github.com/Twingate/kubernetes-operator/commit/7933a9bba38b5da2a94c5b5ec7e87477348d49b9))

- Bump syrupy from 4.9.0 to 4.9.1 ([#584](https://github.com/Twingate/kubernetes-operator/pull/584),
  [`08df2f9`](https://github.com/Twingate/kubernetes-operator/commit/08df2f9f524795a88167b9be0d9ddb9f0723024b))

- Bump types-croniter from 5.0.1.20241205 to 5.0.1.20250322
  ([#585](https://github.com/Twingate/kubernetes-operator/pull/585),
  [`bb7d493`](https://github.com/Twingate/kubernetes-operator/commit/bb7d493a66de0c6ae489284a673358f1b4572d2f))

- Bump types-pyyaml from 6.0.12.20241230 to 6.0.12.20250326
  ([#588](https://github.com/Twingate/kubernetes-operator/pull/588),
  [`c49fd2c`](https://github.com/Twingate/kubernetes-operator/commit/c49fd2cfba092a9b8facd12ca70b7b71b892accf))

- Bump types-requests from 2.32.0.20241016 to 2.32.0.20250301
  ([#564](https://github.com/Twingate/kubernetes-operator/pull/564),
  [`93ee2e8`](https://github.com/Twingate/kubernetes-operator/commit/93ee2e891ec032093e137afbbf6fb0779d578113))

- Bump types-requests from 2.32.0.20250301 to 2.32.0.20250306
  ([#567](https://github.com/Twingate/kubernetes-operator/pull/567),
  [`ba28c63`](https://github.com/Twingate/kubernetes-operator/commit/ba28c63387a0b11da0555bde87b975ac91695001))

- Bump tzdata from 2023.3 to 2025.2
  ([`5436813`](https://github.com/Twingate/kubernetes-operator/commit/5436813d8994667d8c3c45b75b15ab3a081d6dfd))

- Fix dockerfile “AS” to uppercase
  ([`1a17ce6`](https://github.com/Twingate/kubernetes-operator/commit/1a17ce61fcdfc1065ced8448929fa24c29b046fc))

### Documentation

- Fix typo 'closing' → 'cloning' in Helm installation section
  ([#575](https://github.com/Twingate/kubernetes-operator/pull/575),
  [`5fb8062`](https://github.com/Twingate/kubernetes-operator/commit/5fb8062b26edd9856b6e75b1376bd69a544798c8))

### Features

- Support for removing annotation from service + integration tests
  ([#534](https://github.com/Twingate/kubernetes-operator/pull/534),
  [`e6cd068`](https://github.com/Twingate/kubernetes-operator/commit/e6cd06849d5e958be082c97706e25a04374272ec))

- **crds**: Add categories to CRDs and fix indentation for shortNames to enhance organization and
  readability in Kubernetes resources
  ([#579](https://github.com/Twingate/kubernetes-operator/pull/579),
  [`f8255f1`](https://github.com/Twingate/kubernetes-operator/commit/f8255f16cd512aa823def435bb73aa04c1284098))


## v0.17.0 (2025-02-25)

### Chores

- Bump azure/setup-helm from 4.2.0 to 4.3.0
  ([#552](https://github.com/Twingate/kubernetes-operator/pull/552),
  [`4213684`](https://github.com/Twingate/kubernetes-operator/commit/4213684cbf49e17f7f913954dce892d8cfc2433e))

- Bump bandit from 1.8.2 to 1.8.3 ([#547](https://github.com/Twingate/kubernetes-operator/pull/547),
  [`89411ed`](https://github.com/Twingate/kubernetes-operator/commit/89411ed0c72912ead747f87138358ffee418c7f0))

- Bump danger/danger-js from 12.3.3 to 12.3.4
  ([#545](https://github.com/Twingate/kubernetes-operator/pull/545),
  [`1241bf6`](https://github.com/Twingate/kubernetes-operator/commit/1241bf66bf1986a15fdfdcfc30b57ae665d1412b))

- Bump factory-boy from 3.3.1 to 3.3.3
  ([#536](https://github.com/Twingate/kubernetes-operator/pull/536),
  [`aef79b1`](https://github.com/Twingate/kubernetes-operator/commit/aef79b1dcfeb54936d7b0980d3855770f125c49d))

- Bump github.com/gruntwork-io/terratest from 0.48.1 to 0.48.2
  ([#537](https://github.com/Twingate/kubernetes-operator/pull/537),
  [`1c81b05`](https://github.com/Twingate/kubernetes-operator/commit/1c81b05f3cbe87cdb680e1461428a2e2983fbd49))

- Bump google-cloud-artifact-registry from 1.14.0 to 1.15.0
  ([#546](https://github.com/Twingate/kubernetes-operator/pull/546),
  [`06eecb6`](https://github.com/Twingate/kubernetes-operator/commit/06eecb62aee4edfecb2bb25f9e989d87b1da2292))

- Bump google-cloud-artifact-registry from 1.15.0 to 1.15.1
  ([#553](https://github.com/Twingate/kubernetes-operator/pull/553),
  [`19f687b`](https://github.com/Twingate/kubernetes-operator/commit/19f687b00c177c1d7455e4d7f6242f642797e117))

- Bump gql from 3.5.0 to 3.5.1 ([#550](https://github.com/Twingate/kubernetes-operator/pull/550),
  [`6d6a860`](https://github.com/Twingate/kubernetes-operator/commit/6d6a860f11fc037bdc49f28a823e6ef77a72468b))

- Bump kubernetes from 32.0.0 to 32.0.1
  ([#549](https://github.com/Twingate/kubernetes-operator/pull/549),
  [`fe454e9`](https://github.com/Twingate/kubernetes-operator/commit/fe454e92ee0c601c66c4a677a848c00990b3f2b8))

- Bump mypy from 1.14.1 to 1.15.0 ([#538](https://github.com/Twingate/kubernetes-operator/pull/538),
  [`669bf99`](https://github.com/Twingate/kubernetes-operator/commit/669bf99c77f156985c9f0acecf6ee01b77df0cc2))

- Bump ncipollo/release-action from 1.15.0 to 1.16.0
  ([#557](https://github.com/Twingate/kubernetes-operator/pull/557),
  [`f07184f`](https://github.com/Twingate/kubernetes-operator/commit/f07184f5233b88ac2efe8f2adb766e0942ea10d7))

- Bump pydantic-settings from 2.7.1 to 2.8.0
  ([#554](https://github.com/Twingate/kubernetes-operator/pull/554),
  [`b3109d0`](https://github.com/Twingate/kubernetes-operator/commit/b3109d0cc222114c3f50625dd5798c82c8fe7773))

- Bump pytest-datadir from 1.5.0 to 1.6.1
  ([#541](https://github.com/Twingate/kubernetes-operator/pull/541),
  [`0f1696a`](https://github.com/Twingate/kubernetes-operator/commit/0f1696a358fb20200cc5da47d87f536d48dd682f))

- Bump python-semantic-release from 9.17.0 to 9.18.0
  ([#539](https://github.com/Twingate/kubernetes-operator/pull/539),
  [`7c8a2b5`](https://github.com/Twingate/kubernetes-operator/commit/7c8a2b5d1b9e68267446917e3c467093d721c2fe))

- Bump python-semantic-release from 9.18.0 to 9.19.0
  ([#543](https://github.com/Twingate/kubernetes-operator/pull/543),
  [`2db1f42`](https://github.com/Twingate/kubernetes-operator/commit/2db1f426b5bf96eb0666c28f19de43188f326303))

- Bump python-semantic-release from 9.19.0 to 9.19.1
  ([#544](https://github.com/Twingate/kubernetes-operator/pull/544),
  [`efb99d0`](https://github.com/Twingate/kubernetes-operator/commit/efb99d0bdb1e27163ceddadeb3c1ee7910a7575a))

- Bump python-semantic-release from 9.19.1 to 9.20.0
  ([#548](https://github.com/Twingate/kubernetes-operator/pull/548),
  [`9bfc8e5`](https://github.com/Twingate/kubernetes-operator/commit/9bfc8e5001f499f1da29b30c0a74fcf2ed90ac26))

- Bump python-semantic-release from 9.20.0 to 9.21.0
  ([#558](https://github.com/Twingate/kubernetes-operator/pull/558),
  [`c425b4d`](https://github.com/Twingate/kubernetes-operator/commit/c425b4d0df93fb6a85a4278772d78f9878e57cd8))

- Bump ruff from 0.9.3 to 0.9.4 ([#535](https://github.com/Twingate/kubernetes-operator/pull/535),
  [`141ec37`](https://github.com/Twingate/kubernetes-operator/commit/141ec376096941f3a7d4672e76bdb846535006d9))

- Bump ruff from 0.9.4 to 0.9.5 ([#540](https://github.com/Twingate/kubernetes-operator/pull/540),
  [`98bc251`](https://github.com/Twingate/kubernetes-operator/commit/98bc25126d255b4277e94c427b3eb98d0635683e))

- Bump ruff from 0.9.5 to 0.9.6 ([#542](https://github.com/Twingate/kubernetes-operator/pull/542),
  [`d3e48cf`](https://github.com/Twingate/kubernetes-operator/commit/d3e48cf458115993dd820932eb35d487122f7792))

- Bump ruff from 0.9.6 to 0.9.7 ([#551](https://github.com/Twingate/kubernetes-operator/pull/551),
  [`1f9d351`](https://github.com/Twingate/kubernetes-operator/commit/1f9d351b4abe7cba8d56bdd13ed2e561356bfc0f))

- Bump syrupy from 4.8.1 to 4.8.2 ([#555](https://github.com/Twingate/kubernetes-operator/pull/555),
  [`7590c10`](https://github.com/Twingate/kubernetes-operator/commit/7590c10ec9a5a5fea90565c570eb89aa9f9d89bc))

- Update local dev version of Python to 3.12.9
  ([`a8eb289`](https://github.com/Twingate/kubernetes-operator/commit/a8eb289dd36dbfe8bf3846824f0760f0ca581ddb))

### Documentation

- Improve TwingateResourceAccess CRD descriptions
  ([#559](https://github.com/Twingate/kubernetes-operator/pull/559),
  [`636670d`](https://github.com/Twingate/kubernetes-operator/commit/636670d6ac06f2e9f01f450ae8222325b2eccff7))

### Features

- Add app-version to chart when releasing prod
  ([#560](https://github.com/Twingate/kubernetes-operator/pull/560),
  [`d6302dc`](https://github.com/Twingate/kubernetes-operator/commit/d6302dc81d7932396b3e6d31487ea527f5b7f0f1))


## v0.16.2 (2025-01-28)

### Bug Fixes

- Service annotations update not working
  ([#531](https://github.com/Twingate/kubernetes-operator/pull/531),
  [`48fa93c`](https://github.com/Twingate/kubernetes-operator/commit/48fa93c36331a7a0ec77c48a7ac9116578934460))

### Chores

- Bump bandit from 1.8.0 to 1.8.2 ([#515](https://github.com/Twingate/kubernetes-operator/pull/515),
  [`8e83903`](https://github.com/Twingate/kubernetes-operator/commit/8e8390384ccd6e7573b04b4216e77413552a0f93))

- Bump golang.org/x/net from 0.31.0 to 0.33.0
  ([#523](https://github.com/Twingate/kubernetes-operator/pull/523),
  [`0ff77c5`](https://github.com/Twingate/kubernetes-operator/commit/0ff77c5abc1b74a1eda686b3588aa547edb371f2))

- Bump kubernetes from 31.0.0 to 32.0.0
  ([#527](https://github.com/Twingate/kubernetes-operator/pull/527),
  [`91c5042`](https://github.com/Twingate/kubernetes-operator/commit/91c504295746b2133f4fad6f5d6df74fc2fcf8b4))

- Bump ncipollo/release-action from 1.14.0 to 1.15.0
  ([#511](https://github.com/Twingate/kubernetes-operator/pull/511),
  [`5e7724e`](https://github.com/Twingate/kubernetes-operator/commit/5e7724eabfb954eddfb802ff89051907420f5666))

- Bump orjson from 3.10.13 to 3.10.14
  ([#508](https://github.com/Twingate/kubernetes-operator/pull/508),
  [`8255523`](https://github.com/Twingate/kubernetes-operator/commit/8255523d8733a716f9b4222646e711f15350f5d2))

- Bump orjson from 3.10.14 to 3.10.15
  ([#524](https://github.com/Twingate/kubernetes-operator/pull/524),
  [`0744ad8`](https://github.com/Twingate/kubernetes-operator/commit/0744ad80ee1f87bf8102a7fdf44e0a36afdd9d9a))

- Bump pre-commit from 4.0.1 to 4.1.0
  ([#525](https://github.com/Twingate/kubernetes-operator/pull/525),
  [`bddea4f`](https://github.com/Twingate/kubernetes-operator/commit/bddea4f8d00fd9ccce96eb5cf5592498531e457d))

- Bump pydantic from 2.10.4 to 2.10.5
  ([#510](https://github.com/Twingate/kubernetes-operator/pull/510),
  [`fb33861`](https://github.com/Twingate/kubernetes-operator/commit/fb33861aa308e9924b62b0854b9e48e3e55bbb0c))

- Bump pydantic from 2.10.5 to 2.10.6
  ([#529](https://github.com/Twingate/kubernetes-operator/pull/529),
  [`5d3d000`](https://github.com/Twingate/kubernetes-operator/commit/5d3d000c6c4a8edb4542e5da8bc48755c4162391))

- Bump python-semantic-release from 9.15.2 to 9.16.1
  ([#514](https://github.com/Twingate/kubernetes-operator/pull/514),
  [`b356c73`](https://github.com/Twingate/kubernetes-operator/commit/b356c73ebb8fea8512c053456d0ce8858c27692f))

- Bump python-semantic-release from 9.16.1 to 9.17.0
  ([#532](https://github.com/Twingate/kubernetes-operator/pull/532),
  [`c5c6c83`](https://github.com/Twingate/kubernetes-operator/commit/c5c6c83b6db2a64da4826cb45488ed70097af996))

- Bump responses from 0.25.3 to 0.25.5
  ([#516](https://github.com/Twingate/kubernetes-operator/pull/516),
  [`7d89215`](https://github.com/Twingate/kubernetes-operator/commit/7d892152cc0555c23217eb5eb18ff1b88d2c67c9))

- Bump responses from 0.25.5 to 0.25.6
  ([#521](https://github.com/Twingate/kubernetes-operator/pull/521),
  [`5aabf03`](https://github.com/Twingate/kubernetes-operator/commit/5aabf039adce0dde366017ab6a13559b8cf1a780))

- Bump ruff from 0.8.6 to 0.9.1 ([#513](https://github.com/Twingate/kubernetes-operator/pull/513),
  [`13528a4`](https://github.com/Twingate/kubernetes-operator/commit/13528a45e30c1b5e245d4c05a7958791f5bd1b31))

- Bump ruff from 0.9.1 to 0.9.2 ([#522](https://github.com/Twingate/kubernetes-operator/pull/522),
  [`642e3e5`](https://github.com/Twingate/kubernetes-operator/commit/642e3e5c72f5bca5038692ab67c3050b061986df))

- Bump ruff from 0.9.2 to 0.9.3 ([#528](https://github.com/Twingate/kubernetes-operator/pull/528),
  [`86da11b`](https://github.com/Twingate/kubernetes-operator/commit/86da11b2d837f53f99b09a430afe2581c9da03b3))

- Bump syrupy from 4.8.0 to 4.8.1 ([#512](https://github.com/Twingate/kubernetes-operator/pull/512),
  [`edb984a`](https://github.com/Twingate/kubernetes-operator/commit/edb984a9c4bfa546fd801d7535bba1edd7e0a9a6))

- Bump virtualenv from 20.24.5 to 20.26.6
  ([#517](https://github.com/Twingate/kubernetes-operator/pull/517),
  [`37adbf5`](https://github.com/Twingate/kubernetes-operator/commit/37adbf5933a16d680102b4e5003213fe723fd194))

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

- Make integration tests more stable
  ([#506](https://github.com/Twingate/kubernetes-operator/pull/506),
  [`ffa70d4`](https://github.com/Twingate/kubernetes-operator/commit/ffa70d461b9340eafa8a483c133d0799afaf7b3f))

### Chores

- Bump mypy from 1.14.0 to 1.14.1 ([#503](https://github.com/Twingate/kubernetes-operator/pull/503),
  [`891239e`](https://github.com/Twingate/kubernetes-operator/commit/891239eb0973916d9a4c30711a5f7d1d6d94894e))

- Bump orjson from 3.10.12 to 3.10.13
  ([#501](https://github.com/Twingate/kubernetes-operator/pull/501),
  [`5199b1f`](https://github.com/Twingate/kubernetes-operator/commit/5199b1f88be9dc9df7c881af7b220b69505724a7))

- Bump pydantic-settings from 2.7.0 to 2.7.1
  ([#502](https://github.com/Twingate/kubernetes-operator/pull/502),
  [`868e2e3`](https://github.com/Twingate/kubernetes-operator/commit/868e2e3532fd65bfe43613338715a9457df40580))

- Bump ruff from 0.8.4 to 0.8.5 ([#505](https://github.com/Twingate/kubernetes-operator/pull/505),
  [`31f694f`](https://github.com/Twingate/kubernetes-operator/commit/31f694faa3acc1f1cd6eeb9c4990fe22e05ffc0e))

- Bump ruff from 0.8.5 to 0.8.6 ([#507](https://github.com/Twingate/kubernetes-operator/pull/507),
  [`98892cb`](https://github.com/Twingate/kubernetes-operator/commit/98892cb8ada9425be86bb174ba5087afcac0a721))


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

- Bump github.com/gruntwork-io/terratest from 0.48.0 to 0.48.1
  ([#493](https://github.com/Twingate/kubernetes-operator/pull/493),
  [`a4deb4d`](https://github.com/Twingate/kubernetes-operator/commit/a4deb4dafbff8eedbcec55cc61a2d723a6760a1e))

- Bump jinja2 from 3.1.4 to 3.1.5 ([#499](https://github.com/Twingate/kubernetes-operator/pull/499),
  [`05913e3`](https://github.com/Twingate/kubernetes-operator/commit/05913e3cc3aea2b814c8c1e656d64a743d36597c))

- Bump mypy from 1.13.0 to 1.14.0 ([#498](https://github.com/Twingate/kubernetes-operator/pull/498),
  [`e8adb5d`](https://github.com/Twingate/kubernetes-operator/commit/e8adb5d597f7df70dc4db1168a5fdb4a8f9c11e2))

- Bump pydantic from 2.10.3 to 2.10.4
  ([#496](https://github.com/Twingate/kubernetes-operator/pull/496),
  [`519ee4f`](https://github.com/Twingate/kubernetes-operator/commit/519ee4f31c0cefa14de0d381c582741efd489d3d))

- Bump pyupgrade from 3.19.0 to 3.19.1
  ([#492](https://github.com/Twingate/kubernetes-operator/pull/492),
  [`ffbca7f`](https://github.com/Twingate/kubernetes-operator/commit/ffbca7fad06a2347b9517c8330d34c23a8d5b292))

- Bump ruff from 0.8.3 to 0.8.4 ([#497](https://github.com/Twingate/kubernetes-operator/pull/497),
  [`5b03229`](https://github.com/Twingate/kubernetes-operator/commit/5b03229ba0c7f843af7213070c4a6c242ed1c26a))

- Fix typo in release script
  ([`8e31713`](https://github.com/Twingate/kubernetes-operator/commit/8e3171375aee8724df0490ee076b58c216eb9d09))

- Switch to markdownlint-cli
  ([`4468f96`](https://github.com/Twingate/kubernetes-operator/commit/4468f96f2512d5850170c335258a36ef408c4723))

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

- Bump golang.org/x/crypto from 0.21.0 to 0.31.0
  ([#482](https://github.com/Twingate/kubernetes-operator/pull/482),
  [`48b5ad1`](https://github.com/Twingate/kubernetes-operator/commit/48b5ad113fb5167d7c692cebdbe2c14bdc53ca5f))

- Bump google-cloud-artifact-registry from 1.13.1 to 1.14.0
  ([#484](https://github.com/Twingate/kubernetes-operator/pull/484),
  [`baeb563`](https://github.com/Twingate/kubernetes-operator/commit/baeb563f2fa9dc64fb69c78f5f3a2345ba3b0c12))

- Bump kopf from 1.37.3 to 1.37.4 ([#488](https://github.com/Twingate/kubernetes-operator/pull/488),
  [`f17436f`](https://github.com/Twingate/kubernetes-operator/commit/f17436fbd595fea4dc579acd3ded66bfad588ccb))

- Bump pydantic-settings from 2.6.1 to 2.7.0
  ([#483](https://github.com/Twingate/kubernetes-operator/pull/483),
  [`f43c3c3`](https://github.com/Twingate/kubernetes-operator/commit/f43c3c3f050ea5ab143fa6badc559f546e9ebda8))

- Bump python-semantic-release from 9.15.1 to 9.15.2
  ([#489](https://github.com/Twingate/kubernetes-operator/pull/489),
  [`d911b83`](https://github.com/Twingate/kubernetes-operator/commit/d911b83ca3ad6240a56544033ab8cebbcb1d9d55))

- Bump ruff from 0.8.2 to 0.8.3 ([#485](https://github.com/Twingate/kubernetes-operator/pull/485),
  [`8a600a0`](https://github.com/Twingate/kubernetes-operator/commit/8a600a09a7e16cb5b04d43eb807f3c8770a8be25))

- Fix README markdownlint warnings
  ([`c623d90`](https://github.com/Twingate/kubernetes-operator/commit/c623d9030e3266ab3ca4e141aee7d25079d3c228))

### Features

- Allow using a pull thru docker cache with the imagepolicy schedule
  ([#477](https://github.com/Twingate/kubernetes-operator/pull/477),
  [`81fdb30`](https://github.com/Twingate/kubernetes-operator/commit/81fdb30022b8b7185c7148607b61dd1b7c5bb755))

- Enable Configuration of Kopf Watch Settings via Environment Variables
  ([#487](https://github.com/Twingate/kubernetes-operator/pull/487),
  [`3da4225`](https://github.com/Twingate/kubernetes-operator/commit/3da4225865e767fe8ca74477f477bf2b3ca8fc02))


## v0.13.0 (2024-12-06)

### Bug Fixes

- Update Chart version
  ([`0e0efe5`](https://github.com/Twingate/kubernetes-operator/commit/0e0efe5e9a858497c085c5f6ce3788ad43a3d934))

### Chores

- Bump aiohttp from 3.10.2 to 3.10.11
  ([#462](https://github.com/Twingate/kubernetes-operator/pull/462),
  [`efddeee`](https://github.com/Twingate/kubernetes-operator/commit/efddeee21cb4557e7ac00c0a39e433a62c2b17c0))

- Bump bandit from 1.7.10 to 1.8.0
  ([#468](https://github.com/Twingate/kubernetes-operator/pull/468),
  [`5f9af7f`](https://github.com/Twingate/kubernetes-operator/commit/5f9af7f1ef1dfcb9e3d5f2351a83afbe614b5f30))

- Bump google-cloud-artifact-registry from 1.13.0 to 1.13.1
  ([#459](https://github.com/Twingate/kubernetes-operator/pull/459),
  [`b2e5621`](https://github.com/Twingate/kubernetes-operator/commit/b2e5621390e62e9fe2ed5c562662f9643d6c4b22))

- Bump kopf from 1.37.2 to 1.37.3 ([#460](https://github.com/Twingate/kubernetes-operator/pull/460),
  [`1261c0f`](https://github.com/Twingate/kubernetes-operator/commit/1261c0f0680bf9c8a0d13af81ae78f86a33981fe))

- Bump orjson from 3.10.11 to 3.10.12
  ([#465](https://github.com/Twingate/kubernetes-operator/pull/465),
  [`c1aa7cc`](https://github.com/Twingate/kubernetes-operator/commit/c1aa7ccbd3f380aec0a673ab83933812e489b991))

- Bump pydantic from 2.10.0 to 2.10.2
  ([#467](https://github.com/Twingate/kubernetes-operator/pull/467),
  [`f889dcb`](https://github.com/Twingate/kubernetes-operator/commit/f889dcb1e09052388672bfcddb58a3c1fa6366aa))

- Bump pydantic from 2.10.2 to 2.10.3
  ([#473](https://github.com/Twingate/kubernetes-operator/pull/473),
  [`ba5c4cb`](https://github.com/Twingate/kubernetes-operator/commit/ba5c4cb88abb7e6215fd17177c680e586f6cfd57))

- Bump pydantic from 2.9.2 to 2.10.0
  ([#461](https://github.com/Twingate/kubernetes-operator/pull/461),
  [`c2f4be3`](https://github.com/Twingate/kubernetes-operator/commit/c2f4be3bb3e805e06705c8b95e3c374aacf49754))

- Bump pytest from 8.3.3 to 8.3.4 ([#470](https://github.com/Twingate/kubernetes-operator/pull/470),
  [`42a9aa2`](https://github.com/Twingate/kubernetes-operator/commit/42a9aa239ce3f9545c77561a54d7aed58bc1364b))

- Bump python-semantic-release from 9.12.1 to 9.12.2
  ([#454](https://github.com/Twingate/kubernetes-operator/pull/454),
  [`dfff3dd`](https://github.com/Twingate/kubernetes-operator/commit/dfff3dd3121dda7cab9ee67f970e49eec55085d8))

- Bump python-semantic-release from 9.12.2 to 9.14.0
  ([#457](https://github.com/Twingate/kubernetes-operator/pull/457),
  [`527a398`](https://github.com/Twingate/kubernetes-operator/commit/527a398ae04297ebc6c9b70d1e2db83fd460a617))

- Bump python-semantic-release from 9.14.0 to 9.15.0
  ([#471](https://github.com/Twingate/kubernetes-operator/pull/471),
  [`32a804f`](https://github.com/Twingate/kubernetes-operator/commit/32a804f7990b86a023041384e7215166516a3b8e))

- Bump python-semantic-release from 9.15.0 to 9.15.1
  ([#472](https://github.com/Twingate/kubernetes-operator/pull/472),
  [`422fae7`](https://github.com/Twingate/kubernetes-operator/commit/422fae7dde116b7a78d9d91b881b0b4f6bc4f0c9))

- Bump ruff from 0.7.2 to 0.7.3 ([#455](https://github.com/Twingate/kubernetes-operator/pull/455),
  [`5ddf682`](https://github.com/Twingate/kubernetes-operator/commit/5ddf682d023f2b38cf7ea98e9ddd34607f1a2a56))

- Bump ruff from 0.7.3 to 0.7.4 ([#458](https://github.com/Twingate/kubernetes-operator/pull/458),
  [`d45896f`](https://github.com/Twingate/kubernetes-operator/commit/d45896fb710f65f66252c3522ba1d233ddc11cf9))

- Bump ruff from 0.7.4 to 0.8.1 ([#469](https://github.com/Twingate/kubernetes-operator/pull/469),
  [`66f49ff`](https://github.com/Twingate/kubernetes-operator/commit/66f49ff436b35be5df0c8cb9462c1087deb48d6b))

- Bump ruff from 0.8.1 to 0.8.2 ([#476](https://github.com/Twingate/kubernetes-operator/pull/476),
  [`15ea2ed`](https://github.com/Twingate/kubernetes-operator/commit/15ea2edc331cc6cc3f0ba0176676abdf9986639b))

- Bump syrupy from 4.7.2 to 4.8.0 ([#466](https://github.com/Twingate/kubernetes-operator/pull/466),
  [`33127ba`](https://github.com/Twingate/kubernetes-operator/commit/33127ba1c5398930c8e96f1624ebf797b748df39))

- Bump types-croniter from 4.0.0.20241030 to 5.0.1.20241205
  ([#475](https://github.com/Twingate/kubernetes-operator/pull/475),
  [`0fd2aad`](https://github.com/Twingate/kubernetes-operator/commit/0fd2aad9fa28b274d4fa57eda68f97f22bd31148))

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


## v0.12.0 (2024-11-04)

### Bug Fixes

- TwingateResourceAccess deletion fail if resource has been deleted
  ([#420](https://github.com/Twingate/kubernetes-operator/pull/420),
  [`2ede60f`](https://github.com/Twingate/kubernetes-operator/commit/2ede60fbe9f2443151e4f71d1ab5bc6f5539e0e2))

### Chores

- Bump aiohttp from 3.9.4 to 3.10.2
  ([#384](https://github.com/Twingate/kubernetes-operator/pull/384),
  [`619aa3c`](https://github.com/Twingate/kubernetes-operator/commit/619aa3cf8069d6d1b432594aa70c62535330d264))

- Bump bandit from 1.7.9 to 1.7.10
  ([#414](https://github.com/Twingate/kubernetes-operator/pull/414),
  [`e2bac71`](https://github.com/Twingate/kubernetes-operator/commit/e2bac71ae1356c6abe6155dda5f3dffa1fa5d133))

- Bump certifi from 2023.7.22 to 2024.7.4
  ([#348](https://github.com/Twingate/kubernetes-operator/pull/348),
  [`ee89e41`](https://github.com/Twingate/kubernetes-operator/commit/ee89e419a7801cfeefd8a631e1685e4b944ef487))

- Bump croniter from 2.0.5 to 2.0.7
  ([#357](https://github.com/Twingate/kubernetes-operator/pull/357),
  [`9b72cec`](https://github.com/Twingate/kubernetes-operator/commit/9b72cec553f6f03103e73ed151a08a760c9426c7))

- Bump croniter from 2.0.7 to 3.0.0
  ([#365](https://github.com/Twingate/kubernetes-operator/pull/365),
  [`f033f9c`](https://github.com/Twingate/kubernetes-operator/commit/f033f9c587636aa3f4750a66d6c5ffa951da521d))

- Bump croniter from 3.0.0 to 3.0.1
  ([#368](https://github.com/Twingate/kubernetes-operator/pull/368),
  [`aa7c32d`](https://github.com/Twingate/kubernetes-operator/commit/aa7c32d3764775ed03860247a81871497781a4bc))

- Bump croniter from 3.0.1 to 3.0.3
  ([#371](https://github.com/Twingate/kubernetes-operator/pull/371),
  [`c5715cf`](https://github.com/Twingate/kubernetes-operator/commit/c5715cf85e8d457699870923dd61cadba94acb5f))

- Bump croniter from 3.0.3 to 3.0.4
  ([#442](https://github.com/Twingate/kubernetes-operator/pull/442),
  [`5dfadee`](https://github.com/Twingate/kubernetes-operator/commit/5dfadeea58ab1c6fceb07a1eca7c0836ecb62ea8))

- Bump croniter from 3.0.4 to 5.0.1
  ([#448](https://github.com/Twingate/kubernetes-operator/pull/448),
  [`1e1c26b`](https://github.com/Twingate/kubernetes-operator/commit/1e1c26b5bdcaf3083cf3e4453842f64637436d9f))

- Bump factory-boy from 3.3.0 to 3.3.1
  ([#387](https://github.com/Twingate/kubernetes-operator/pull/387),
  [`5dfdd7e`](https://github.com/Twingate/kubernetes-operator/commit/5dfdd7ed2cb4be6910c88416873d58fde4fc730e))

- Bump github.com/gruntwork-io/terratest from 0.46.16 to 0.47.0
  ([#353](https://github.com/Twingate/kubernetes-operator/pull/353),
  [`1becc60`](https://github.com/Twingate/kubernetes-operator/commit/1becc605fd89d48b8a5cbdd533b46124864009fd))

- Bump github.com/gruntwork-io/terratest from 0.47.0 to 0.47.1
  ([#393](https://github.com/Twingate/kubernetes-operator/pull/393),
  [`7038f3a`](https://github.com/Twingate/kubernetes-operator/commit/7038f3afa48a87a2e046a6b4b25ac59b9243d236))

- Bump github.com/gruntwork-io/terratest from 0.47.1 to 0.47.2
  ([#419](https://github.com/Twingate/kubernetes-operator/pull/419),
  [`e218644`](https://github.com/Twingate/kubernetes-operator/commit/e218644f7db742080f497424db5ac346db015578))

- Bump google-cloud-artifact-registry from 1.11.3 to 1.11.4
  ([#351](https://github.com/Twingate/kubernetes-operator/pull/351),
  [`d1d14ad`](https://github.com/Twingate/kubernetes-operator/commit/d1d14ad667853adb89fc962deceb17bb95e328f4))

- Bump google-cloud-artifact-registry from 1.11.4 to 1.11.5
  ([#380](https://github.com/Twingate/kubernetes-operator/pull/380),
  [`86014ce`](https://github.com/Twingate/kubernetes-operator/commit/86014ce5b11d789295fb6cd3bd9cc515280e789b))

- Bump google-cloud-artifact-registry from 1.11.5 to 1.12.0
  ([#441](https://github.com/Twingate/kubernetes-operator/pull/441),
  [`7afc39f`](https://github.com/Twingate/kubernetes-operator/commit/7afc39f7d2be456ef71040a1a747094104ea4b78))

- Bump google-cloud-artifact-registry from 1.12.0 to 1.13.0
  ([#447](https://github.com/Twingate/kubernetes-operator/pull/447),
  [`89678be`](https://github.com/Twingate/kubernetes-operator/commit/89678bea9d9ce0790c8135882bec19e7c9000685))

- Bump kubernetes from 30.1.0 to 31.0.0
  ([#409](https://github.com/Twingate/kubernetes-operator/pull/409),
  [`f6d0500`](https://github.com/Twingate/kubernetes-operator/commit/f6d0500284ec9a2ce9183e31b898fdd70246cf3f))

- Bump mypy from 1.10.1 to 1.11.0 ([#361](https://github.com/Twingate/kubernetes-operator/pull/361),
  [`aa27f17`](https://github.com/Twingate/kubernetes-operator/commit/aa27f1782f33746ccd7fdd0ca7b0d33a5772d3a3))

- Bump mypy from 1.11.0 to 1.11.1 ([#379](https://github.com/Twingate/kubernetes-operator/pull/379),
  [`3b4587f`](https://github.com/Twingate/kubernetes-operator/commit/3b4587fe2a66f2e31be7afbf44ad7a0bb5b4d36a))

- Bump mypy from 1.11.1 to 1.11.2 ([#392](https://github.com/Twingate/kubernetes-operator/pull/392),
  [`7a27253`](https://github.com/Twingate/kubernetes-operator/commit/7a27253a7b70bf9204399497f59736d677c37063))

- Bump mypy from 1.11.2 to 1.12.0 ([#428](https://github.com/Twingate/kubernetes-operator/pull/428),
  [`fd0e177`](https://github.com/Twingate/kubernetes-operator/commit/fd0e17701618f0695ffca9fc6098a38a3d547a0a))

- Bump mypy from 1.12.0 to 1.12.1 ([#436](https://github.com/Twingate/kubernetes-operator/pull/436),
  [`9040578`](https://github.com/Twingate/kubernetes-operator/commit/90405786bc27ff26f4a7f745f4f4885df7f7c8c7))

- Bump mypy from 1.12.1 to 1.13.0 ([#439](https://github.com/Twingate/kubernetes-operator/pull/439),
  [`91d9126`](https://github.com/Twingate/kubernetes-operator/commit/91d9126e7ad1a473183b0be3f71132ed4e37ee3f))

- Bump orjson from 3.10.10 to 3.10.11
  ([#451](https://github.com/Twingate/kubernetes-operator/pull/451),
  [`32b353e`](https://github.com/Twingate/kubernetes-operator/commit/32b353eb067e6f424908ca7e773cc71c1fe3b428))

- Bump orjson from 3.10.6 to 3.10.7
  ([#383](https://github.com/Twingate/kubernetes-operator/pull/383),
  [`f44d7dc`](https://github.com/Twingate/kubernetes-operator/commit/f44d7dc4a16454c4e6a63fc3259cc97a8a9eda54))

- Bump orjson from 3.10.7 to 3.10.9
  ([#437](https://github.com/Twingate/kubernetes-operator/pull/437),
  [`8b91596`](https://github.com/Twingate/kubernetes-operator/commit/8b915962974b8abd32c55ab8655e73b7fb3a51d2))

- Bump orjson from 3.10.9 to 3.10.10
  ([#440](https://github.com/Twingate/kubernetes-operator/pull/440),
  [`376dd8a`](https://github.com/Twingate/kubernetes-operator/commit/376dd8ac237fcbabaa08b8d72cac73b2eda979bf))

- Bump pre-commit from 3.7.1 to 3.8.0
  ([#376](https://github.com/Twingate/kubernetes-operator/pull/376),
  [`d13be35`](https://github.com/Twingate/kubernetes-operator/commit/d13be351b2a5b5602eb9b22d7571f0064b82effc))

- Bump pre-commit from 3.8.0 to 4.0.1
  ([#425](https://github.com/Twingate/kubernetes-operator/pull/425),
  [`7b6ab07`](https://github.com/Twingate/kubernetes-operator/commit/7b6ab076db82ae93b678c7a67ab347b0c56650be))

- Bump pydantic from 2.8.0 to 2.8.2
  ([#345](https://github.com/Twingate/kubernetes-operator/pull/345),
  [`633d0c3`](https://github.com/Twingate/kubernetes-operator/commit/633d0c3b102d7c4ebd54fdc97ba8671ddb45b0d6))

- Bump pydantic from 2.8.2 to 2.9.0
  ([#398](https://github.com/Twingate/kubernetes-operator/pull/398),
  [`ee34d0e`](https://github.com/Twingate/kubernetes-operator/commit/ee34d0ef06d7e002c482672590ef8ac39df77de6))

- Bump pydantic from 2.9.0 to 2.9.1
  ([#401](https://github.com/Twingate/kubernetes-operator/pull/401),
  [`077be19`](https://github.com/Twingate/kubernetes-operator/commit/077be196e6686c352060c0822b810831353573ba))

- Bump pydantic from 2.9.1 to 2.9.2
  ([#408](https://github.com/Twingate/kubernetes-operator/pull/408),
  [`04b6514`](https://github.com/Twingate/kubernetes-operator/commit/04b65140b9eb1cd5a58330fb9f046e05fc33ae2d))

- Bump pydantic-settings from 2.3.4 to 2.4.0
  ([#377](https://github.com/Twingate/kubernetes-operator/pull/377),
  [`b19e5b5`](https://github.com/Twingate/kubernetes-operator/commit/b19e5b5c0b044d76e7ec92245d7012ee76ee5b85))

- Bump pydantic-settings from 2.4.0 to 2.5.2
  ([#405](https://github.com/Twingate/kubernetes-operator/pull/405),
  [`1bbcbe0`](https://github.com/Twingate/kubernetes-operator/commit/1bbcbe01169c8b3b9fe38e4b43070fadb154b582))

- Bump pydantic-settings from 2.5.2 to 2.6.0
  ([#433](https://github.com/Twingate/kubernetes-operator/pull/433),
  [`c51fce3`](https://github.com/Twingate/kubernetes-operator/commit/c51fce3d7a76cbf25c67a395d6a4339626b9a1f9))

- Bump pydantic-settings from 2.6.0 to 2.6.1
  ([#450](https://github.com/Twingate/kubernetes-operator/pull/450),
  [`b42d9f5`](https://github.com/Twingate/kubernetes-operator/commit/b42d9f5d9bdbc64315e3d272750a450aac639f11))

- Bump pytest from 8.2.2 to 8.3.1 ([#359](https://github.com/Twingate/kubernetes-operator/pull/359),
  [`1abcfd8`](https://github.com/Twingate/kubernetes-operator/commit/1abcfd82392f5f62b07b847c3cb76826a1066d58))

- Bump pytest from 8.3.1 to 8.3.2 ([#369](https://github.com/Twingate/kubernetes-operator/pull/369),
  [`0e3c380`](https://github.com/Twingate/kubernetes-operator/commit/0e3c3801c272bb927229bb0938e5d8f0c52f0b8a))

- Bump pytest from 8.3.2 to 8.3.3 ([#404](https://github.com/Twingate/kubernetes-operator/pull/404),
  [`cb46953`](https://github.com/Twingate/kubernetes-operator/commit/cb469536636728777d87616397bc64774a5a8618))

- Bump pytest-randomly from 3.15.0 to 3.16.0
  ([#445](https://github.com/Twingate/kubernetes-operator/pull/445),
  [`1de3f80`](https://github.com/Twingate/kubernetes-operator/commit/1de3f809d866282baf1899a3de64abd94ccef1ee))

- Bump python-semantic-release from 9.10.0 to 9.10.1
  ([#426](https://github.com/Twingate/kubernetes-operator/pull/426),
  [`53bf3bb`](https://github.com/Twingate/kubernetes-operator/commit/53bf3bb34fdcf0e24e6358620a4621143eaf12c8))

- Bump python-semantic-release from 9.10.1 to 9.11.0
  ([#429](https://github.com/Twingate/kubernetes-operator/pull/429),
  [`f85f585`](https://github.com/Twingate/kubernetes-operator/commit/f85f585223e11213df6b4a84bd995351d8593dde))

- Bump python-semantic-release from 9.11.0 to 9.11.1
  ([#431](https://github.com/Twingate/kubernetes-operator/pull/431),
  [`4d841d5`](https://github.com/Twingate/kubernetes-operator/commit/4d841d53cfaf420677efd9ba587e4de42a0890ca))

- Bump python-semantic-release from 9.11.1 to 9.12.0
  ([#434](https://github.com/Twingate/kubernetes-operator/pull/434),
  [`fda0a57`](https://github.com/Twingate/kubernetes-operator/commit/fda0a57153d196c64f0e41c0cbcb5ffa95b5a4b8))

- Bump python-semantic-release from 9.8.3 to 9.8.4
  ([#346](https://github.com/Twingate/kubernetes-operator/pull/346),
  [`db13a96`](https://github.com/Twingate/kubernetes-operator/commit/db13a9660e449110b6c31d835a29c8f84f65d2b0))

- Bump python-semantic-release from 9.8.4 to 9.8.5
  ([#350](https://github.com/Twingate/kubernetes-operator/pull/350),
  [`629260a`](https://github.com/Twingate/kubernetes-operator/commit/629260a7fbc5e0438dc4112d6849be5d77b2f29a))

- Bump python-semantic-release from 9.8.5 to 9.8.6
  ([#363](https://github.com/Twingate/kubernetes-operator/pull/363),
  [`5d99d5d`](https://github.com/Twingate/kubernetes-operator/commit/5d99d5dced95a1ae4126460927353403f63e6f36))

- Bump python-semantic-release from 9.8.6 to 9.8.7
  ([#388](https://github.com/Twingate/kubernetes-operator/pull/388),
  [`ec6f1fd`](https://github.com/Twingate/kubernetes-operator/commit/ec6f1fd7e09aeb2a92120510bb2909ce29e1b77d))

- Bump python-semantic-release from 9.8.7 to 9.8.8
  ([#395](https://github.com/Twingate/kubernetes-operator/pull/395),
  [`e36c1de`](https://github.com/Twingate/kubernetes-operator/commit/e36c1de4272a3cbde6dc4fb259e309cce0666727))

- Bump python-semantic-release from 9.8.8 to 9.8.9
  ([#417](https://github.com/Twingate/kubernetes-operator/pull/417),
  [`e41a483`](https://github.com/Twingate/kubernetes-operator/commit/e41a483a94033fc0a6402f16443e55f45b4e7d90))

- Bump python-semantic-release from 9.8.9 to 9.9.0
  ([#418](https://github.com/Twingate/kubernetes-operator/pull/418),
  [`0eac57c`](https://github.com/Twingate/kubernetes-operator/commit/0eac57c57a01d7b1afa57aaddd97a6d8cc49526c))

- Bump python-semantic-release from 9.9.0 to 9.10.0
  ([#424](https://github.com/Twingate/kubernetes-operator/pull/424),
  [`c3808e2`](https://github.com/Twingate/kubernetes-operator/commit/c3808e27279d706f6860c58a401e7e5317f221c5))

- Bump pyupgrade from 3.16.0 to 3.17.0
  ([#374](https://github.com/Twingate/kubernetes-operator/pull/374),
  [`0eed8c8`](https://github.com/Twingate/kubernetes-operator/commit/0eed8c81bc2c9f230e29979d3e6c639602c3ac26))

- Bump pyupgrade from 3.17.0 to 3.18.0
  ([#430](https://github.com/Twingate/kubernetes-operator/pull/430),
  [`f716a95`](https://github.com/Twingate/kubernetes-operator/commit/f716a95649826a2ba18e2746163aa4a176ec5e5c))

- Bump pyupgrade from 3.18.0 to 3.19.0
  ([#438](https://github.com/Twingate/kubernetes-operator/pull/438),
  [`5b12b4e`](https://github.com/Twingate/kubernetes-operator/commit/5b12b4eaf60691eacfd7b3c220026bdd90cdfae5))

- Bump ruff from 0.5.0 to 0.5.1 ([#349](https://github.com/Twingate/kubernetes-operator/pull/349),
  [`357a4d6`](https://github.com/Twingate/kubernetes-operator/commit/357a4d67269be50a43c4f57f87d3ab8c684d45ac))

- Bump ruff from 0.5.1 to 0.5.2 ([#354](https://github.com/Twingate/kubernetes-operator/pull/354),
  [`e7c76ae`](https://github.com/Twingate/kubernetes-operator/commit/e7c76ae13459424d0f98bab59def5b6d93fd59a2))

- Bump ruff from 0.5.2 to 0.5.3 ([#358](https://github.com/Twingate/kubernetes-operator/pull/358),
  [`d7ef48a`](https://github.com/Twingate/kubernetes-operator/commit/d7ef48aa0d4b9b38efc6351758c6afc6ca27bd10))

- Bump ruff from 0.5.3 to 0.5.4 ([#360](https://github.com/Twingate/kubernetes-operator/pull/360),
  [`15c6827`](https://github.com/Twingate/kubernetes-operator/commit/15c68276cc9dc669854ce715de012f64733c3414))

- Bump ruff from 0.5.4 to 0.5.5 ([#372](https://github.com/Twingate/kubernetes-operator/pull/372),
  [`b48ce95`](https://github.com/Twingate/kubernetes-operator/commit/b48ce95f46e7143e743932f1809c821a16ead024))

- Bump ruff from 0.5.5 to 0.5.6 ([#381](https://github.com/Twingate/kubernetes-operator/pull/381),
  [`4c4cd41`](https://github.com/Twingate/kubernetes-operator/commit/4c4cd41531c1a65bb3009f00e904ad9f554964f8))

- Bump ruff from 0.5.6 to 0.5.7 ([#382](https://github.com/Twingate/kubernetes-operator/pull/382),
  [`0c1fc84`](https://github.com/Twingate/kubernetes-operator/commit/0c1fc844206d844467aa44cf78afb4673c3ea850))

- Bump ruff from 0.5.7 to 0.6.2 ([#391](https://github.com/Twingate/kubernetes-operator/pull/391),
  [`0c26ca3`](https://github.com/Twingate/kubernetes-operator/commit/0c26ca3ccc25500ad59019eea5d39312e85ffe7c))

- Bump ruff from 0.6.2 to 0.6.3 ([#394](https://github.com/Twingate/kubernetes-operator/pull/394),
  [`373aa1f`](https://github.com/Twingate/kubernetes-operator/commit/373aa1fe671ca0ced889702498aed752622a384d))

- Bump ruff from 0.6.3 to 0.6.4 ([#399](https://github.com/Twingate/kubernetes-operator/pull/399),
  [`de387fd`](https://github.com/Twingate/kubernetes-operator/commit/de387fd30cc4561b132363f60fc4d9cc37ab640a))

- Bump ruff from 0.6.4 to 0.6.5 ([#406](https://github.com/Twingate/kubernetes-operator/pull/406),
  [`89e9efe`](https://github.com/Twingate/kubernetes-operator/commit/89e9efed571958b743621268af202ed2a295e134))

- Bump ruff from 0.6.5 to 0.6.6 ([#410](https://github.com/Twingate/kubernetes-operator/pull/410),
  [`bf3f798`](https://github.com/Twingate/kubernetes-operator/commit/bf3f798137c1f6f9b86c5cbe7cb078e3896c7406))

- Bump ruff from 0.6.6 to 0.6.7 ([#411](https://github.com/Twingate/kubernetes-operator/pull/411),
  [`61ab430`](https://github.com/Twingate/kubernetes-operator/commit/61ab430eb97f2b69a65b31ef3da0672f6e18f5fd))

- Bump ruff from 0.6.7 to 0.6.8 ([#416](https://github.com/Twingate/kubernetes-operator/pull/416),
  [`fa8c761`](https://github.com/Twingate/kubernetes-operator/commit/fa8c7619605e13115831673a621fbcaa8c7ee7be))

- Bump ruff from 0.6.8 to 0.6.9 ([#422](https://github.com/Twingate/kubernetes-operator/pull/422),
  [`0dd8063`](https://github.com/Twingate/kubernetes-operator/commit/0dd80630f2adcc7ae754d327aea282f4cf81d622))

- Bump ruff from 0.6.9 to 0.7.0 ([#435](https://github.com/Twingate/kubernetes-operator/pull/435),
  [`fcc1ffe`](https://github.com/Twingate/kubernetes-operator/commit/fcc1ffe09175ce5901e018acf60110b10f559597))

- Bump ruff from 0.7.0 to 0.7.1 ([#443](https://github.com/Twingate/kubernetes-operator/pull/443),
  [`f429127`](https://github.com/Twingate/kubernetes-operator/commit/f4291270d879860d8688704640e49219cc52535a))

- Bump ruff from 0.7.1 to 0.7.2 ([#452](https://github.com/Twingate/kubernetes-operator/pull/452),
  [`08995b7`](https://github.com/Twingate/kubernetes-operator/commit/08995b71b80cddd22a2c1ecf89575bdd9e23a985))

- Bump setuptools from 68.2.0 to 70.0.0
  ([#355](https://github.com/Twingate/kubernetes-operator/pull/355),
  [`69664ac`](https://github.com/Twingate/kubernetes-operator/commit/69664acb92ec6df2ba2b3147277aa842397f5670))

- Bump syrupy from 4.6.1 to 4.6.4 ([#389](https://github.com/Twingate/kubernetes-operator/pull/389),
  [`71209d7`](https://github.com/Twingate/kubernetes-operator/commit/71209d73e99419bca13afaab94239fa2a6d38025))

- Bump syrupy from 4.6.4 to 4.7.1 ([#390](https://github.com/Twingate/kubernetes-operator/pull/390),
  [`84c794a`](https://github.com/Twingate/kubernetes-operator/commit/84c794a73bb090b2b5811a01f28e253b00440ca0))

- Bump syrupy from 4.7.1 to 4.7.2 ([#423](https://github.com/Twingate/kubernetes-operator/pull/423),
  [`9cdf0bb`](https://github.com/Twingate/kubernetes-operator/commit/9cdf0bb84716d4892e27a27f8a1c5f479760dfc0))

- Bump tenacity from 8.4.2 to 8.5.0
  ([#347](https://github.com/Twingate/kubernetes-operator/pull/347),
  [`c73fa81`](https://github.com/Twingate/kubernetes-operator/commit/c73fa817b722460a129eaadc28f6d5735023c9bb))

- Bump tenacity from 8.5.0 to 9.0.0
  ([#373](https://github.com/Twingate/kubernetes-operator/pull/373),
  [`4fbc93a`](https://github.com/Twingate/kubernetes-operator/commit/4fbc93a8909592aaeb11542d1c27ec815a9c2cc6))

- Bump types-croniter from 2.0.0.20240423 to 2.0.5.20240717
  ([#356](https://github.com/Twingate/kubernetes-operator/pull/356),
  [`627834f`](https://github.com/Twingate/kubernetes-operator/commit/627834ff5dbe0487c37ba18688b3fb7d09b90d19))

- Bump types-croniter from 2.0.5.20240717 to 2.0.5.20240722
  ([#362](https://github.com/Twingate/kubernetes-operator/pull/362),
  [`865295c`](https://github.com/Twingate/kubernetes-operator/commit/865295cc5fc38102dcafcfe268c0a199d3c3f983))

- Bump types-croniter from 2.0.5.20240722 to 3.0.3.20240731
  ([#378](https://github.com/Twingate/kubernetes-operator/pull/378),
  [`60d6f18`](https://github.com/Twingate/kubernetes-operator/commit/60d6f18cd4b5b15722407daff2e22e1ecc429bda))

- Bump types-croniter from 3.0.3.20240731 to 3.0.4.20241027
  ([#444](https://github.com/Twingate/kubernetes-operator/pull/444),
  [`c5c35ec`](https://github.com/Twingate/kubernetes-operator/commit/c5c35eccb27ab5b53adc03d40f769a143dbeece9))

- Bump types-croniter from 3.0.4.20241027 to 4.0.0.20241030
  ([#449](https://github.com/Twingate/kubernetes-operator/pull/449),
  [`d9812fa`](https://github.com/Twingate/kubernetes-operator/commit/d9812fa064a89f8f7f423f0ec6ef7aa181aee927))

- Bump types-requests from 2.32.0.20240622 to 2.32.0.20240712
  ([#352](https://github.com/Twingate/kubernetes-operator/pull/352),
  [`62a0dcc`](https://github.com/Twingate/kubernetes-operator/commit/62a0dcc4bd46028ffb1c35410565312db5b6ca1a))

- Bump types-requests from 2.32.0.20240712 to 2.32.0.20240905
  ([#396](https://github.com/Twingate/kubernetes-operator/pull/396),
  [`7118358`](https://github.com/Twingate/kubernetes-operator/commit/7118358fe59b141d85dc0525e9f3ef1603a2ee7b))

- Bump types-requests from 2.32.0.20240905 to 2.32.0.20240907
  ([#402](https://github.com/Twingate/kubernetes-operator/pull/402),
  [`8adb4ee`](https://github.com/Twingate/kubernetes-operator/commit/8adb4ee67a8d31650ce498f0f36c4d760d9f6934))

- Bump types-requests from 2.32.0.20240907 to 2.32.0.20240914
  ([#407](https://github.com/Twingate/kubernetes-operator/pull/407),
  [`420449c`](https://github.com/Twingate/kubernetes-operator/commit/420449c03c0412003f0a64c021a759c48c837848))

- Bump types-requests from 2.32.0.20240914 to 2.32.0.20241016
  ([#432](https://github.com/Twingate/kubernetes-operator/pull/432),
  [`c31c74c`](https://github.com/Twingate/kubernetes-operator/commit/c31c74cc6b122780ec3cb34d8ff04f91faf86f9f))

- Re-enable poetry package mode setting to be False
  ([`7473698`](https://github.com/Twingate/kubernetes-operator/commit/74736982fde898144aac51f4e3fd15da603c9e6d))

### Features

- Nicer `kubectl get` for TwingateResource and TwingateConnector
  ([#366](https://github.com/Twingate/kubernetes-operator/pull/366),
  [`7f5697f`](https://github.com/Twingate/kubernetes-operator/commit/7f5697f3ae37b6cc1ad0a26815794d4096a7f6f8))

- Support referencing TwingateGroup from TwingateResourceAccess
  ([#412](https://github.com/Twingate/kubernetes-operator/pull/412),
  [`c27f98f`](https://github.com/Twingate/kubernetes-operator/commit/c27f98f02dabd353d2bf55d0d5f9ae803c58ec0b))

- TwingateGroup object - support creating groups via k8s object
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

- Bump mypy from 1.10.0 to 1.10.1 ([#335](https://github.com/Twingate/kubernetes-operator/pull/335),
  [`2bf326a`](https://github.com/Twingate/kubernetes-operator/commit/2bf326ad4458cf11bb130301d636aa3ed0da9514))

- Bump orjson from 3.10.5 to 3.10.6
  ([#342](https://github.com/Twingate/kubernetes-operator/pull/342),
  [`f7c24bd`](https://github.com/Twingate/kubernetes-operator/commit/f7c24bd77b4399c2e41868ce6de0f39aeec34f10))

- Bump pydantic from 2.7.4 to 2.8.0
  ([#341](https://github.com/Twingate/kubernetes-operator/pull/341),
  [`db3d023`](https://github.com/Twingate/kubernetes-operator/commit/db3d0235118fd08d615220d24ab49bbcbcc92b98))

- Bump pydantic-settings from 2.3.3 to 2.3.4
  ([#334](https://github.com/Twingate/kubernetes-operator/pull/334),
  [`93f0747`](https://github.com/Twingate/kubernetes-operator/commit/93f0747c513f29bd7fe6efa50cfb4109f05d45f8))

- Bump ruff from 0.4.10 to 0.5.0 ([#340](https://github.com/Twingate/kubernetes-operator/pull/340),
  [`353060a`](https://github.com/Twingate/kubernetes-operator/commit/353060a6542768a70b6290d877ebc46bb5950465))

- Bump tenacity from 8.4.1 to 8.4.2
  ([#336](https://github.com/Twingate/kubernetes-operator/pull/336),
  [`3b91830`](https://github.com/Twingate/kubernetes-operator/commit/3b9183015f6fe73f93fbdbbddf582ea9880b2ec4))


## v0.11.4 (2024-06-24)

### Bug Fixes

- Allow connectors to run under Restricted pod-security policy
  ([#329](https://github.com/Twingate/kubernetes-operator/pull/329),
  [`14302df`](https://github.com/Twingate/kubernetes-operator/commit/14302df61105d8ce4d4423d03626008c1df7e8b1))

### Chores

- Bump bandit from 1.7.8 to 1.7.9 ([#321](https://github.com/Twingate/kubernetes-operator/pull/321),
  [`64523df`](https://github.com/Twingate/kubernetes-operator/commit/64523df8b1f60e2cafee6202744bb651c73de492))

- Bump danger/danger-js from 12.2.0 to 12.3.0
  ([#295](https://github.com/Twingate/kubernetes-operator/pull/295),
  [`a752166`](https://github.com/Twingate/kubernetes-operator/commit/a752166824394c90e321b748933228e8473f4ccc))

- Bump danger/danger-js from 12.3.0 to 12.3.1
  ([#311](https://github.com/Twingate/kubernetes-operator/pull/311),
  [`9309f19`](https://github.com/Twingate/kubernetes-operator/commit/9309f1989c71bcbccf09af2d249e9c9ea078903b))

- Bump danger/danger-js from 12.3.1 to 12.3.3
  ([#331](https://github.com/Twingate/kubernetes-operator/pull/331),
  [`ff0a8e1`](https://github.com/Twingate/kubernetes-operator/commit/ff0a8e14f86a49374987c1404dcda66c404426c0))

- Bump github.com/gruntwork-io/terratest from 0.46.14 to 0.46.15
  ([#297](https://github.com/Twingate/kubernetes-operator/pull/297),
  [`9142339`](https://github.com/Twingate/kubernetes-operator/commit/9142339f39abb350d06253a704cefa9ae493fc82))

- Bump kubernetes from 29.0.0 to 30.1.0
  ([#314](https://github.com/Twingate/kubernetes-operator/pull/314),
  [`b5fccd0`](https://github.com/Twingate/kubernetes-operator/commit/b5fccd0f68de5e57b075f6da8f31a506dd9c3592))

- Bump orjson from 3.10.3 to 3.10.4
  ([#317](https://github.com/Twingate/kubernetes-operator/pull/317),
  [`2c9f2e7`](https://github.com/Twingate/kubernetes-operator/commit/2c9f2e7fa07ac5811ebd950a389605602dbddc86))

- Bump orjson from 3.10.4 to 3.10.5
  ([#322](https://github.com/Twingate/kubernetes-operator/pull/322),
  [`1c0a0ea`](https://github.com/Twingate/kubernetes-operator/commit/1c0a0ea711d840e4f5acf961b6aa269cd88d180c))

- Bump pydantic from 2.7.1 to 2.7.2
  ([#303](https://github.com/Twingate/kubernetes-operator/pull/303),
  [`c5d4648`](https://github.com/Twingate/kubernetes-operator/commit/c5d46486eeda8d63ddd3eade8c765da8aa9e24b7))

- Bump pydantic from 2.7.2 to 2.7.3
  ([#308](https://github.com/Twingate/kubernetes-operator/pull/308),
  [`9569663`](https://github.com/Twingate/kubernetes-operator/commit/9569663df45cfe6fb0553c78ae2e81fa0f1c593e))

- Bump pydantic from 2.7.3 to 2.7.4
  ([#319](https://github.com/Twingate/kubernetes-operator/pull/319),
  [`e88c317`](https://github.com/Twingate/kubernetes-operator/commit/e88c317afbfe4a0216c55dafa558b7c65da20d0f))

- Bump pydantic-settings from 2.2.1 to 2.3.0
  ([#307](https://github.com/Twingate/kubernetes-operator/pull/307),
  [`a4eb52e`](https://github.com/Twingate/kubernetes-operator/commit/a4eb52e6d7388627ff84047cfecf106db22f4322))

- Bump pydantic-settings from 2.3.0 to 2.3.1
  ([#313](https://github.com/Twingate/kubernetes-operator/pull/313),
  [`c172a45`](https://github.com/Twingate/kubernetes-operator/commit/c172a45983ba1fce6aecf7f7813652a9b25eaced))

- Bump pydantic-settings from 2.3.1 to 2.3.2
  ([#318](https://github.com/Twingate/kubernetes-operator/pull/318),
  [`2733fb5`](https://github.com/Twingate/kubernetes-operator/commit/2733fb52192ac9eca8d558f8a8f82f325b9c3590))

- Bump pydantic-settings from 2.3.2 to 2.3.3
  ([#320](https://github.com/Twingate/kubernetes-operator/pull/320),
  [`3dcfe30`](https://github.com/Twingate/kubernetes-operator/commit/3dcfe30c9345fb397b1e68c4c064bc5c3782e30d))

- Bump pytest from 8.2.1 to 8.2.2 ([#310](https://github.com/Twingate/kubernetes-operator/pull/310),
  [`48a2b78`](https://github.com/Twingate/kubernetes-operator/commit/48a2b7888eae2fd55c286725928563ef7177f890))

- Bump python-semantic-release from 9.7.3 to 9.8.0
  ([#301](https://github.com/Twingate/kubernetes-operator/pull/301),
  [`7c2ebec`](https://github.com/Twingate/kubernetes-operator/commit/7c2ebecce3ecf6160245c955aa47251a23181ca9))

- Bump python-semantic-release from 9.8.0 to 9.8.1
  ([#309](https://github.com/Twingate/kubernetes-operator/pull/309),
  [`56d33da`](https://github.com/Twingate/kubernetes-operator/commit/56d33dacd98ac01d59d5999c6f274103cbd2be85))

- Bump python-semantic-release from 9.8.1 to 9.8.2
  ([#325](https://github.com/Twingate/kubernetes-operator/pull/325),
  [`204df1b`](https://github.com/Twingate/kubernetes-operator/commit/204df1bd4eb1c2fd5d4598af8f85df04888770ac))

- Bump python-semantic-release from 9.8.2 to 9.8.3
  ([#328](https://github.com/Twingate/kubernetes-operator/pull/328),
  [`af0a52f`](https://github.com/Twingate/kubernetes-operator/commit/af0a52f40f562f325b97c83199d27362403cb82e))

- Bump pyupgrade from 3.15.2 to 3.16.0
  ([#316](https://github.com/Twingate/kubernetes-operator/pull/316),
  [`201d69a`](https://github.com/Twingate/kubernetes-operator/commit/201d69a0fb2ac2244c422f3a4699e7b0894d6946))

- Bump requests from 2.31.0 to 2.32.1
  ([#294](https://github.com/Twingate/kubernetes-operator/pull/294),
  [`7935746`](https://github.com/Twingate/kubernetes-operator/commit/7935746bd45f867cefe78d77abed472fbda948b4))

- Bump requests from 2.32.1 to 2.32.2
  ([#296](https://github.com/Twingate/kubernetes-operator/pull/296),
  [`18038ea`](https://github.com/Twingate/kubernetes-operator/commit/18038ea6936a08a511fa15363879b378b9fa3dc7))

- Bump requests from 2.32.2 to 2.32.3
  ([#304](https://github.com/Twingate/kubernetes-operator/pull/304),
  [`2aa20be`](https://github.com/Twingate/kubernetes-operator/commit/2aa20be75fe6e93e37425d6d4ccaeb8de9813f4d))

- Bump responses from 0.25.0 to 0.25.2
  ([#315](https://github.com/Twingate/kubernetes-operator/pull/315),
  [`be5ff6e`](https://github.com/Twingate/kubernetes-operator/commit/be5ff6e28cf562cc29ee650ada7fdeb0c53d9204))

- Bump responses from 0.25.2 to 0.25.3
  ([#324](https://github.com/Twingate/kubernetes-operator/pull/324),
  [`7f636e4`](https://github.com/Twingate/kubernetes-operator/commit/7f636e4f333fffacaff0d37dbe08da4c6d90258a))

- Bump ruff from 0.4.4 to 0.4.5 ([#298](https://github.com/Twingate/kubernetes-operator/pull/298),
  [`ad48803`](https://github.com/Twingate/kubernetes-operator/commit/ad48803f51b18d451f340dd9f522fc227b204a9c))

- Bump ruff from 0.4.5 to 0.4.6 ([#302](https://github.com/Twingate/kubernetes-operator/pull/302),
  [`317a197`](https://github.com/Twingate/kubernetes-operator/commit/317a197bf9dbffdd86ec8b76024de7893674186c))

- Bump ruff from 0.4.6 to 0.4.7 ([#306](https://github.com/Twingate/kubernetes-operator/pull/306),
  [`b04e7ee`](https://github.com/Twingate/kubernetes-operator/commit/b04e7ee8d8dd98710ddc5d29d3257a066f2199c6))

- Bump ruff from 0.4.7 to 0.4.8 ([#312](https://github.com/Twingate/kubernetes-operator/pull/312),
  [`ab409ac`](https://github.com/Twingate/kubernetes-operator/commit/ab409acebd453f9afd066eb81784943c8daf410f))

- Bump ruff from 0.4.8 to 0.4.9 ([#323](https://github.com/Twingate/kubernetes-operator/pull/323),
  [`fa36571`](https://github.com/Twingate/kubernetes-operator/commit/fa3657197dc552d28a9e8088c0452effc1326fd6))

- Bump ruff from 0.4.9 to 0.4.10 ([#332](https://github.com/Twingate/kubernetes-operator/pull/332),
  [`0584245`](https://github.com/Twingate/kubernetes-operator/commit/0584245905f92f44fc328fb2cbe48991091f4a03))

- Bump tenacity from 8.3.0 to 8.4.1
  ([#326](https://github.com/Twingate/kubernetes-operator/pull/326),
  [`54ccc57`](https://github.com/Twingate/kubernetes-operator/commit/54ccc574545f073a8f3d700247e00de1aeb91994))

- Bump types-requests from 2.31.0.20240406 to 2.32.0.20240521
  ([#293](https://github.com/Twingate/kubernetes-operator/pull/293),
  [`1751140`](https://github.com/Twingate/kubernetes-operator/commit/1751140d8d8060957ccdaec30f7441d9c9ff6048))

- Bump types-requests from 2.32.0.20240521 to 2.32.0.20240523
  ([#299](https://github.com/Twingate/kubernetes-operator/pull/299),
  [`f4d7c25`](https://github.com/Twingate/kubernetes-operator/commit/f4d7c259d820e25058f1ade43fe548c548f9bae0))

- Bump types-requests from 2.32.0.20240523 to 2.32.0.20240602
  ([#305](https://github.com/Twingate/kubernetes-operator/pull/305),
  [`b965d94`](https://github.com/Twingate/kubernetes-operator/commit/b965d940b7b938d0da352dcae326551358b4ee5a))

- Bump types-requests from 2.32.0.20240602 to 2.32.0.20240622
  ([#333](https://github.com/Twingate/kubernetes-operator/pull/333),
  [`bda3eca`](https://github.com/Twingate/kubernetes-operator/commit/bda3ecab987090e6ad6fa625b01e603dd24e3bfd))

- Bump urllib3 from 2.1.0 to 2.2.2
  ([#327](https://github.com/Twingate/kubernetes-operator/pull/327),
  [`7632e25`](https://github.com/Twingate/kubernetes-operator/commit/7632e25d86ef097b972561feb1266603f152d7ea))

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

- Bump python-semantic-release from 9.7.1 to 9.7.2
  ([#284](https://github.com/Twingate/kubernetes-operator/pull/284),
  [`defa346`](https://github.com/Twingate/kubernetes-operator/commit/defa3465ea6d439244a3366063d6fdc525dc1828))

- Bump python-semantic-release from 9.7.2 to 9.7.3
  ([#288](https://github.com/Twingate/kubernetes-operator/pull/288),
  [`2f856a6`](https://github.com/Twingate/kubernetes-operator/commit/2f856a658e72247177c607529acd4d3d0e14b3cc))

- Increase test coverage ([#285](https://github.com/Twingate/kubernetes-operator/pull/285),
  [`28b69f5`](https://github.com/Twingate/kubernetes-operator/commit/28b69f52ce812c43721383397497ac4616f41faa))


## v0.11.2 (2024-05-12)

### Bug Fixes

- TwingateResourceAccess only updating every 10h and not immediately
  ([#283](https://github.com/Twingate/kubernetes-operator/pull/283),
  [`2809bb9`](https://github.com/Twingate/kubernetes-operator/commit/2809bb99417370d767077ed082848038abd03273))

### Chores

- Bump pre-commit from 3.7.0 to 3.7.1
  ([#282](https://github.com/Twingate/kubernetes-operator/pull/282),
  [`2957dd5`](https://github.com/Twingate/kubernetes-operator/commit/2957dd5a402d82ab6dac5ff2bf09219f2464145a))

- Bump ruff from 0.4.3 to 0.4.4 ([#280](https://github.com/Twingate/kubernetes-operator/pull/280),
  [`261998c`](https://github.com/Twingate/kubernetes-operator/commit/261998c4b84615418d707672a58a8cf65ccfde8d))


## v0.11.1 (2024-05-08)

### Bug Fixes

- TwingateResourceAccess timer too frequent
  ([`c1645f4`](https://github.com/Twingate/kubernetes-operator/commit/c1645f4a9a5aa43e26ac7ecbe0a2f0a6d0743bc8))


## v0.11.0 (2024-05-07)

### Chores

- Bump danger/danger-js from 12.1.0 to 12.2.0
  ([#272](https://github.com/Twingate/kubernetes-operator/pull/272),
  [`a5b573a`](https://github.com/Twingate/kubernetes-operator/commit/a5b573a8d143b58675743c0406c676467ca36bb8))

- Bump jinja2 from 3.1.3 to 3.1.4 ([#276](https://github.com/Twingate/kubernetes-operator/pull/276),
  [`98723bd`](https://github.com/Twingate/kubernetes-operator/commit/98723bd78b61112494b6606c9ff19a8cb094253c))

- Bump orjson from 3.10.2 to 3.10.3
  ([#274](https://github.com/Twingate/kubernetes-operator/pull/274),
  [`98826e4`](https://github.com/Twingate/kubernetes-operator/commit/98826e46127313b78c2595eaea3e18170c5c6a67))

- Bump python-semantic-release from 9.6.0 to 9.7.0
  ([#273](https://github.com/Twingate/kubernetes-operator/pull/273),
  [`f2f6681`](https://github.com/Twingate/kubernetes-operator/commit/f2f6681f757cf23d46a7176e57c4c485e21f9d30))

- Bump python-semantic-release from 9.7.0 to 9.7.1
  ([#277](https://github.com/Twingate/kubernetes-operator/pull/277),
  [`ca97d74`](https://github.com/Twingate/kubernetes-operator/commit/ca97d74de284c44b3fe3e5cff2faeb4d4b6a5f9d))

- Bump ruff from 0.4.2 to 0.4.3 ([#275](https://github.com/Twingate/kubernetes-operator/pull/275),
  [`f05639e`](https://github.com/Twingate/kubernetes-operator/commit/f05639ebb3785f691ea053df579b2272d83cfbf4))

- Bump tenacity from 8.2.3 to 8.3.0
  ([#278](https://github.com/Twingate/kubernetes-operator/pull/278),
  [`f2b8ba9`](https://github.com/Twingate/kubernetes-operator/commit/f2b8ba909daadbe68ccbd6780125d6f228b9fa3c))

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

- Bump orjson from 3.10.1 to 3.10.2
  ([#268](https://github.com/Twingate/kubernetes-operator/pull/268),
  [`1bf81a3`](https://github.com/Twingate/kubernetes-operator/commit/1bf81a33b5a6a4344e406862caff803772347291))

- Bump pydantic from 2.7.0 to 2.7.1
  ([#260](https://github.com/Twingate/kubernetes-operator/pull/260),
  [`3f42d4e`](https://github.com/Twingate/kubernetes-operator/commit/3f42d4e1567972919f526a1b86204c804ebb1f04))

- Bump pytest from 8.1.1 to 8.2.0 ([#266](https://github.com/Twingate/kubernetes-operator/pull/266),
  [`0b591f8`](https://github.com/Twingate/kubernetes-operator/commit/0b591f8dc058016908226af0064ab06dfe721f59))

- Bump python-semantic-release from 9.4.2 to 9.5.0
  ([#258](https://github.com/Twingate/kubernetes-operator/pull/258),
  [`e5b292d`](https://github.com/Twingate/kubernetes-operator/commit/e5b292d548c7ee347c0ea759b4a3ada35c484c0e))

- Bump python-semantic-release from 9.5.0 to 9.6.0
  ([#267](https://github.com/Twingate/kubernetes-operator/pull/267),
  [`98b925e`](https://github.com/Twingate/kubernetes-operator/commit/98b925e06d2d471e239591f6441625dc362b3cc7))

- Bump ruff from 0.4.1 to 0.4.2 ([#263](https://github.com/Twingate/kubernetes-operator/pull/263),
  [`5ddd936`](https://github.com/Twingate/kubernetes-operator/commit/5ddd9369ad55f9506aa69d3a8a5f961ab0d6abd3))

- Bump types-croniter from 2.0.0.20240321 to 2.0.0.20240423
  ([#259](https://github.com/Twingate/kubernetes-operator/pull/259),
  [`4c42521`](https://github.com/Twingate/kubernetes-operator/commit/4c4252107da145f624b27361746be66ee79a1506))

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

- Bump croniter from 2.0.3 to 2.0.5
  ([#257](https://github.com/Twingate/kubernetes-operator/pull/257),
  [`d26366f`](https://github.com/Twingate/kubernetes-operator/commit/d26366f1faeee80939d95d01b10a0ac5b03a3d04))

- Bump danger/danger-js from 11.3.1 to 12.1.0
  ([#253](https://github.com/Twingate/kubernetes-operator/pull/253),
  [`9cd9a8c`](https://github.com/Twingate/kubernetes-operator/commit/9cd9a8c85d3b95115d39586bdb155358eed252cc))

- Bump github.com/gruntwork-io/terratest from 0.46.13 to 0.46.14
  ([#261](https://github.com/Twingate/kubernetes-operator/pull/261),
  [`d346c48`](https://github.com/Twingate/kubernetes-operator/commit/d346c4862be2b42221a5af80fb7a153261281101))

- Bump golang.org/x/net from 0.17.0 to 0.23.0
  ([#255](https://github.com/Twingate/kubernetes-operator/pull/255),
  [`f7cfd19`](https://github.com/Twingate/kubernetes-operator/commit/f7cfd192fc41f7f1ffb6101f94d4293739a0a2e1))

- Bump idna from 3.4 to 3.7 ([#248](https://github.com/Twingate/kubernetes-operator/pull/248),
  [`8fb2baa`](https://github.com/Twingate/kubernetes-operator/commit/8fb2baa7f49400fcc963d63c9cf2e75701862eaf))

- Bump orjson from 3.10.0 to 3.10.1
  ([#252](https://github.com/Twingate/kubernetes-operator/pull/252),
  [`f4e8420`](https://github.com/Twingate/kubernetes-operator/commit/f4e84205a27e23753d347538d8f62b6fac6d43bb))

- Bump pydantic from 2.6.4 to 2.7.0
  ([#250](https://github.com/Twingate/kubernetes-operator/pull/250),
  [`de76253`](https://github.com/Twingate/kubernetes-operator/commit/de7625309afe94c2a0d429986185aaf9222bdb67))

- Bump python-semantic-release from 9.4.1 to 9.4.2
  ([#251](https://github.com/Twingate/kubernetes-operator/pull/251),
  [`d64708e`](https://github.com/Twingate/kubernetes-operator/commit/d64708e127dd73364d21498737ebd4d71b3c4e23))

- Bump ruff from 0.3.5 to 0.3.7 ([#249](https://github.com/Twingate/kubernetes-operator/pull/249),
  [`03542a2`](https://github.com/Twingate/kubernetes-operator/commit/03542a2e8ad1441b64ae5b7eb779e71132859dd8))

- Bump ruff from 0.3.7 to 0.4.1 ([#256](https://github.com/Twingate/kubernetes-operator/pull/256),
  [`cb2dff2`](https://github.com/Twingate/kubernetes-operator/commit/cb2dff2a0eccdb50c2546a1682bf9d48e65e4f75))

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

- Bump python-semantic-release from 9.4.0 to 9.4.1
  ([#241](https://github.com/Twingate/kubernetes-operator/pull/241),
  [`28ec499`](https://github.com/Twingate/kubernetes-operator/commit/28ec499cf1950b1d29bdca3f0da3e7b205cb40ab))

- Bump types-requests from 2.31.0.20240403 to 2.31.0.20240406
  ([#242](https://github.com/Twingate/kubernetes-operator/pull/242),
  [`5bc9e9d`](https://github.com/Twingate/kubernetes-operator/commit/5bc9e9d26e992d67643d1bb4d927afba80e53916))

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

- Bump python-semantic-release from 9.3.1 to 9.4.0
  ([#229](https://github.com/Twingate/kubernetes-operator/pull/229),
  [`70d6b69`](https://github.com/Twingate/kubernetes-operator/commit/70d6b692de48dbf6030015ff0e31e0d6ea8cfedf))

- Bump ruff from 0.3.4 to 0.3.5 ([#230](https://github.com/Twingate/kubernetes-operator/pull/230),
  [`b5075d6`](https://github.com/Twingate/kubernetes-operator/commit/b5075d6dc3194205f1f4c590b34ef19399b55a59))

- Bump types-requests from 2.31.0.20240311 to 2.31.0.20240402
  ([#231](https://github.com/Twingate/kubernetes-operator/pull/231),
  [`bceef26`](https://github.com/Twingate/kubernetes-operator/commit/bceef261d0d5f2fd99d0bf3e0a92d28166ad0411))

- Bump types-requests from 2.31.0.20240402 to 2.31.0.20240403
  ([#235](https://github.com/Twingate/kubernetes-operator/pull/235),
  [`72c9c41`](https://github.com/Twingate/kubernetes-operator/commit/72c9c4164dd098e3e7a05ce535b73729e34f6d1a))

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

- TwingateConnector - allow defining extra pod annotations with `podAnnotations`
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

- Bump bandit from 1.7.7 to 1.7.8 ([#202](https://github.com/Twingate/kubernetes-operator/pull/202),
  [`c7ab9e3`](https://github.com/Twingate/kubernetes-operator/commit/c7ab9e3cc5c41bda1a2649293c0082ceab1f1811))

- Bump croniter from 2.0.2 to 2.0.3
  ([#207](https://github.com/Twingate/kubernetes-operator/pull/207),
  [`9016f41`](https://github.com/Twingate/kubernetes-operator/commit/9016f412913e2f8c0dbc37aadf04a1fe98064469))

- Bump dependabot/fetch-metadata from 1 to 2
  ([#212](https://github.com/Twingate/kubernetes-operator/pull/212),
  [`25bbe4c`](https://github.com/Twingate/kubernetes-operator/commit/25bbe4cffeb16c0d1fbb1d54604b08afa1a1f488))

- Bump github.com/gruntwork-io/terratest from 0.46.12 to 0.46.13
  ([#211](https://github.com/Twingate/kubernetes-operator/pull/211),
  [`d16c8ba`](https://github.com/Twingate/kubernetes-operator/commit/d16c8ba782f95ed84c44a8fc70b398d482001443))

- Bump github.com/gruntwork-io/terratest from 0.46.8 to 0.46.12
  ([#208](https://github.com/Twingate/kubernetes-operator/pull/208),
  [`7baa616`](https://github.com/Twingate/kubernetes-operator/commit/7baa616162f3deadb500e08184f6277fb1deb34b))

- Bump google.golang.org/protobuf from 1.31.0 to 1.33.0
  ([#194](https://github.com/Twingate/kubernetes-operator/pull/194),
  [`ca78968`](https://github.com/Twingate/kubernetes-operator/commit/ca78968f167c99fc1bcf4fa637e47a8c94bb3f2e))

- Bump mypy from 1.8.0 to 1.9.0 ([#196](https://github.com/Twingate/kubernetes-operator/pull/196),
  [`a07f4a8`](https://github.com/Twingate/kubernetes-operator/commit/a07f4a8cb510461ab93dda44c6ca8b465fcc1be1))

- Bump pre-commit from 3.6.2 to 3.7.0
  ([#220](https://github.com/Twingate/kubernetes-operator/pull/220),
  [`81239a5`](https://github.com/Twingate/kubernetes-operator/commit/81239a5aad9a8d2658d02f7190faf634aa06aebe))

- Bump pydantic from 2.6.3 to 2.6.4
  ([#200](https://github.com/Twingate/kubernetes-operator/pull/200),
  [`b14c931`](https://github.com/Twingate/kubernetes-operator/commit/b14c9313215f90c40404a0bbd11d78fd116c6460))

- Bump pytest from 8.1.0 to 8.1.1 ([#197](https://github.com/Twingate/kubernetes-operator/pull/197),
  [`16687d8`](https://github.com/Twingate/kubernetes-operator/commit/16687d84fe0afc22e9cdcf116d7b3a79324f7b3f))

- Bump pytest-cov from 4.1.0 to 5.0.0
  ([#219](https://github.com/Twingate/kubernetes-operator/pull/219),
  [`61e4cc5`](https://github.com/Twingate/kubernetes-operator/commit/61e4cc5ba73231d1cec6bf64c33d6aed372cf19f))

- Bump python-semantic-release from 9.1.1 to 9.2.2
  ([#206](https://github.com/Twingate/kubernetes-operator/pull/206),
  [`eb122f7`](https://github.com/Twingate/kubernetes-operator/commit/eb122f7a46079f3fb867426a8b0e967c493f3478))

- Bump python-semantic-release from 9.2.2 to 9.3.0
  ([#209](https://github.com/Twingate/kubernetes-operator/pull/209),
  [`5f7b54f`](https://github.com/Twingate/kubernetes-operator/commit/5f7b54fad1811007026b7bb04a6da6134644747b))

- Bump python-semantic-release from 9.3.0 to 9.3.1
  ([#221](https://github.com/Twingate/kubernetes-operator/pull/221),
  [`224897d`](https://github.com/Twingate/kubernetes-operator/commit/224897d9b2b7b8ffba37ad3db90f31086229a220))

- Bump pyupgrade from 3.15.1 to 3.15.2
  ([#218](https://github.com/Twingate/kubernetes-operator/pull/218),
  [`5dc320a`](https://github.com/Twingate/kubernetes-operator/commit/5dc320a7a9be39383568eef335d6b1ff11ae2c00))

- Bump ruff from 0.3.1 to 0.3.3 ([#199](https://github.com/Twingate/kubernetes-operator/pull/199),
  [`033c0ff`](https://github.com/Twingate/kubernetes-operator/commit/033c0ff3c3be88c6df5f7298539cb2fc6ec4b0cb))

- Bump ruff from 0.3.3 to 0.3.4 ([#213](https://github.com/Twingate/kubernetes-operator/pull/213),
  [`15ed2b9`](https://github.com/Twingate/kubernetes-operator/commit/15ed2b931cfac64a81ec79f25e1fed822601cf7a))

- Bump types-croniter from 2.0.0.20240106 to 2.0.0.20240318
  ([#203](https://github.com/Twingate/kubernetes-operator/pull/203),
  [`cf5d0e3`](https://github.com/Twingate/kubernetes-operator/commit/cf5d0e35bfbfad0f278c7da66e09702dbb001d95))

- Bump types-croniter from 2.0.0.20240318 to 2.0.0.20240321
  ([#210](https://github.com/Twingate/kubernetes-operator/pull/210),
  [`17790dd`](https://github.com/Twingate/kubernetes-operator/commit/17790dd9f4b1161f4347632dd7fc4b4d5d2def39))

- Bump types-requests from 2.31.0.20240218 to 2.31.0.20240311
  ([#204](https://github.com/Twingate/kubernetes-operator/pull/204),
  [`ad48466`](https://github.com/Twingate/kubernetes-operator/commit/ad484663ff3f8448cfae549ca0454a08ac5327fb))

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

- Bump pytest from 8.0.2 to 8.1.0 ([#182](https://github.com/Twingate/kubernetes-operator/pull/182),
  [`13e479b`](https://github.com/Twingate/kubernetes-operator/commit/13e479bce27f4394e5377b219e4b8b0f7c3deb61))

- Bump pytest-factoryboy from 2.6.0 to 2.7.0
  ([#185](https://github.com/Twingate/kubernetes-operator/pull/185),
  [`22b7f84`](https://github.com/Twingate/kubernetes-operator/commit/22b7f8413696af873258243ba58e2126fa95e43a))

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

- LABEL_CONNECTOR_POD_DELETED isnt set to false after pod recreated
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

- Bump croniter from 2.0.1 to 2.0.2
  ([#172](https://github.com/Twingate/kubernetes-operator/pull/172),
  [`d8e2e88`](https://github.com/Twingate/kubernetes-operator/commit/d8e2e88facd234d65067e14f035b991bae803574))

- Bump google-cloud-artifact-registry from 1.11.1 to 1.11.2
  ([#158](https://github.com/Twingate/kubernetes-operator/pull/158),
  [`2e6a03c`](https://github.com/Twingate/kubernetes-operator/commit/2e6a03c2a4dc4f3d151f45eef1b85407a6bf11f5))

- Bump orjson from 3.9.14 to 3.9.15
  ([#163](https://github.com/Twingate/kubernetes-operator/pull/163),
  [`c8550e5`](https://github.com/Twingate/kubernetes-operator/commit/c8550e5647ea4be80113e904c79ecb35f458e822))

- Bump pre-commit from 3.6.1 to 3.6.2
  ([#154](https://github.com/Twingate/kubernetes-operator/pull/154),
  [`9c188aa`](https://github.com/Twingate/kubernetes-operator/commit/9c188aadc3bdcb03712a948b925d69eb941532f0))

- Bump pydantic from 2.6.1 to 2.6.2
  ([#166](https://github.com/Twingate/kubernetes-operator/pull/166),
  [`3601ec0`](https://github.com/Twingate/kubernetes-operator/commit/3601ec00173ca9fb4905e73856a919bd42a25d6f))

- Bump pydantic from 2.6.2 to 2.6.3
  ([#167](https://github.com/Twingate/kubernetes-operator/pull/167),
  [`cacfec8`](https://github.com/Twingate/kubernetes-operator/commit/cacfec801bd634633aa8156047a05f9c452e541f))

- Bump pydantic-settings from 2.1.0 to 2.2.0
  ([#151](https://github.com/Twingate/kubernetes-operator/pull/151),
  [`c3ccbe4`](https://github.com/Twingate/kubernetes-operator/commit/c3ccbe47da50c7b20edf2d986b130f9d886a6ef6))

- Bump pydantic-settings from 2.2.0 to 2.2.1
  ([#157](https://github.com/Twingate/kubernetes-operator/pull/157),
  [`830b6ac`](https://github.com/Twingate/kubernetes-operator/commit/830b6ac04ed30b249ec87e5cd1ba8af346af7c3b))

- Bump pytest from 8.0.0 to 8.0.1 ([#155](https://github.com/Twingate/kubernetes-operator/pull/155),
  [`a8fcd50`](https://github.com/Twingate/kubernetes-operator/commit/a8fcd50e1da8c83f0bab1dcd6afd00f9f49cbd90))

- Bump pytest from 8.0.1 to 8.0.2 ([#165](https://github.com/Twingate/kubernetes-operator/pull/165),
  [`dc7e2aa`](https://github.com/Twingate/kubernetes-operator/commit/dc7e2aa26b096365fad7d1a580df387e6a6819e9))

- Bump python-semantic-release from 9.1.0 to 9.1.1
  ([#164](https://github.com/Twingate/kubernetes-operator/pull/164),
  [`76a0e07`](https://github.com/Twingate/kubernetes-operator/commit/76a0e07ac378c94e32284a06ef044049806d2886))

- Bump pyupgrade from 3.15.0 to 3.15.1
  ([#153](https://github.com/Twingate/kubernetes-operator/pull/153),
  [`fdfae86`](https://github.com/Twingate/kubernetes-operator/commit/fdfae86e8aff7a3a25873dc53f4c2cbdbc49a5fc))

- Bump ruff from 0.2.1 to 0.2.2 ([#152](https://github.com/Twingate/kubernetes-operator/pull/152),
  [`17f3017`](https://github.com/Twingate/kubernetes-operator/commit/17f30173d39d70cefeabd6d1a3d5c4fb1b810a78))

- Bump ruff from 0.2.2 to 0.3.0 ([#178](https://github.com/Twingate/kubernetes-operator/pull/178),
  [`918311b`](https://github.com/Twingate/kubernetes-operator/commit/918311b74ad654c90205fe34acc93553ab654f79))

- Bump types-requests from 2.31.0.20240125 to 2.31.0.20240218
  ([#149](https://github.com/Twingate/kubernetes-operator/pull/149),
  [`e2e75b8`](https://github.com/Twingate/kubernetes-operator/commit/e2e75b8a1d6782baa2fcd6faa814ee63e845c100))

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

- Bump actions/setup-go from 4 to 5
  ([#141](https://github.com/Twingate/kubernetes-operator/pull/141),
  [`770d518`](https://github.com/Twingate/kubernetes-operator/commit/770d5188aa3ea6e9b6920bfb858fc2580a8b868c))

- Bump actions/setup-python from 4 to 5
  ([#140](https://github.com/Twingate/kubernetes-operator/pull/140),
  [`eae1613`](https://github.com/Twingate/kubernetes-operator/commit/eae161335f08308d128eb32924dadf991da15cf1))

- Bump black from 24.1.1 to 24.2.0
  ([#132](https://github.com/Twingate/kubernetes-operator/pull/132),
  [`9794e04`](https://github.com/Twingate/kubernetes-operator/commit/9794e0402c53fa92cd71161ee848edef67c1d69d))

- Bump crazy-max/ghaction-github-runtime from 2 to 3
  ([#138](https://github.com/Twingate/kubernetes-operator/pull/138),
  [`2833ea9`](https://github.com/Twingate/kubernetes-operator/commit/2833ea953889d943b36d6ea28b97996cfecdd1f4))

- Bump danger/danger-js from 11.3.0 to 11.3.1
  ([#137](https://github.com/Twingate/kubernetes-operator/pull/137),
  [`f8d91fe`](https://github.com/Twingate/kubernetes-operator/commit/f8d91fee7007c13c58bb6f07e204cd8769f193a7))

- Bump google-cloud-artifact-registry from 1.10.0 to 1.11.0
  ([#112](https://github.com/Twingate/kubernetes-operator/pull/112),
  [`f1d74c7`](https://github.com/Twingate/kubernetes-operator/commit/f1d74c78ea665b0beaf4fff178b0760054d99a94))

- Bump google-cloud-artifact-registry from 1.11.0 to 1.11.1
  ([#125](https://github.com/Twingate/kubernetes-operator/pull/125),
  [`dc9c3e2`](https://github.com/Twingate/kubernetes-operator/commit/dc9c3e27492adc22b98869f4a33f83614b8f39d8))

- Bump ncipollo/release-action from 1.13.0 to 1.14.0
  ([#139](https://github.com/Twingate/kubernetes-operator/pull/139),
  [`5ee2ab5`](https://github.com/Twingate/kubernetes-operator/commit/5ee2ab540dafd0ea2a9b405d636e45e33d0a451e))

- Bump orjson from 3.9.12 to 3.9.13
  ([#115](https://github.com/Twingate/kubernetes-operator/pull/115),
  [`c15718b`](https://github.com/Twingate/kubernetes-operator/commit/c15718b4557442a0c672c4cbff208c50986dc486))

- Bump orjson from 3.9.13 to 3.9.14
  ([#134](https://github.com/Twingate/kubernetes-operator/pull/134),
  [`bed5200`](https://github.com/Twingate/kubernetes-operator/commit/bed5200e8eb370ae3fa856a89fcbcafca1c24038))

- Bump pre-commit from 3.6.0 to 3.6.1
  ([#127](https://github.com/Twingate/kubernetes-operator/pull/127),
  [`b3de58d`](https://github.com/Twingate/kubernetes-operator/commit/b3de58ddbda647f5d2f222ee559117e42bba958b))

- Bump pydantic from 2.6.0 to 2.6.1
  ([#117](https://github.com/Twingate/kubernetes-operator/pull/117),
  [`39d499d`](https://github.com/Twingate/kubernetes-operator/commit/39d499d684694abd5df762834b7e6a57b81ed9fb))

- Bump pytest from 7.4.4 to 8.0.0 ([#118](https://github.com/Twingate/kubernetes-operator/pull/118),
  [`0c46fc5`](https://github.com/Twingate/kubernetes-operator/commit/0c46fc5cca7a3459df1093c47dc2d76408d0ef31))

- Bump pytest-sugar from 0.9.7 to 1.0.0
  ([#113](https://github.com/Twingate/kubernetes-operator/pull/113),
  [`6671930`](https://github.com/Twingate/kubernetes-operator/commit/667193002e882ec0d30bf7006e964d5ac9569338))

- Bump python-semantic-release from 8.7.0 to 9.0.3
  ([#126](https://github.com/Twingate/kubernetes-operator/pull/126),
  [`7c4cd35`](https://github.com/Twingate/kubernetes-operator/commit/7c4cd3532170c33a7a5b73d8d99cb9c293e08695))

- Bump python-semantic-release from 9.0.3 to 9.1.0
  ([#142](https://github.com/Twingate/kubernetes-operator/pull/142),
  [`5d95517`](https://github.com/Twingate/kubernetes-operator/commit/5d9551783f2b2979405233eff6c115f6fcc6ce44))

- Bump responses from 0.24.1 to 0.25.0
  ([#133](https://github.com/Twingate/kubernetes-operator/pull/133),
  [`9d01e7c`](https://github.com/Twingate/kubernetes-operator/commit/9d01e7c1287626b23cb706272a2e1c98ba84e560))

- Bump ruff from 0.1.15 to 0.2.0 ([#114](https://github.com/Twingate/kubernetes-operator/pull/114),
  [`88d5dc0`](https://github.com/Twingate/kubernetes-operator/commit/88d5dc0858cd6dcb512b6dedd00181178d268a33))

- Bump ruff from 0.2.0 to 0.2.1 ([#116](https://github.com/Twingate/kubernetes-operator/pull/116),
  [`028a5e8`](https://github.com/Twingate/kubernetes-operator/commit/028a5e8e227b3f29c73e7fca340d17f4a93ff729))

- Bump syrupy from 4.6.0 to 4.6.1 ([#119](https://github.com/Twingate/kubernetes-operator/pull/119),
  [`378f7fc`](https://github.com/Twingate/kubernetes-operator/commit/378f7fcaea1d7208c43612f34c2ef29990c8abe5))

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

- Bump bandit from 1.7.6 to 1.7.7 ([#105](https://github.com/Twingate/kubernetes-operator/pull/105),
  [`f9a682e`](https://github.com/Twingate/kubernetes-operator/commit/f9a682e475abd872e572bfac45e62f7324296bb5))

- Bump black from 23.12.1 to 24.1.1
  ([#108](https://github.com/Twingate/kubernetes-operator/pull/108),
  [`f48e140`](https://github.com/Twingate/kubernetes-operator/commit/f48e14039c02c08e191c6d3438f812b0ed4f84d3))

- Bump kopf from 1.36.2 to 1.37.1 ([#101](https://github.com/Twingate/kubernetes-operator/pull/101),
  [`1c81f10`](https://github.com/Twingate/kubernetes-operator/commit/1c81f10aa9d25eeda25e8f8fa29942eaf3a9a006))

- Bump orjson from 3.9.10 to 3.9.12 ([#99](https://github.com/Twingate/kubernetes-operator/pull/99),
  [`03455ed`](https://github.com/Twingate/kubernetes-operator/commit/03455ed4b77bb86b95046b1b377315ae45c14eb1))

- Bump pydantic from 2.5.3 to 2.6.0
  ([#111](https://github.com/Twingate/kubernetes-operator/pull/111),
  [`b875c14`](https://github.com/Twingate/kubernetes-operator/commit/b875c1453f3a158e52dbb29eb8a8f3f39232518d))

- Bump ruff from 0.1.13 to 0.1.14 ([#100](https://github.com/Twingate/kubernetes-operator/pull/100),
  [`32c783a`](https://github.com/Twingate/kubernetes-operator/commit/32c783a2f3277bfba7472f409245237a8d6ae51d))

- Bump ruff from 0.1.14 to 0.1.15 ([#110](https://github.com/Twingate/kubernetes-operator/pull/110),
  [`397c59d`](https://github.com/Twingate/kubernetes-operator/commit/397c59d50047606b2af473cc20af7405e22d487e))

- Bump types-requests from 2.31.0.20240106 to 2.31.0.20240125
  ([#106](https://github.com/Twingate/kubernetes-operator/pull/106),
  [`76b078c`](https://github.com/Twingate/kubernetes-operator/commit/76b078c4d77d9a05cdf7193101899154442fc339))

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

- ClusterRole definition - create\delete pods and secrets required by Connector functionality
  ([#94](https://github.com/Twingate/kubernetes-operator/pull/94),
  [`d4674fc`](https://github.com/Twingate/kubernetes-operator/commit/d4674fc8ae8e4a702806e1b63c6571abc4f6c936))

- Gql.Client can't be singleton as its not thread-safe
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

- Bump aiohttp from 3.8.5 to 3.8.6 ([#45](https://github.com/Twingate/kubernetes-operator/pull/45),
  [`bf7fcbd`](https://github.com/Twingate/kubernetes-operator/commit/bf7fcbdfc6baebe091f37496ad04898f9e965c78))

- Bump aiohttp from 3.8.6 to 3.9.0 ([#52](https://github.com/Twingate/kubernetes-operator/pull/52),
  [`bae78a0`](https://github.com/Twingate/kubernetes-operator/commit/bae78a03ec00697334d1980a208f691612ce2c61))

- Bump bandit from 1.7.5 to 1.7.6 ([#65](https://github.com/Twingate/kubernetes-operator/pull/65),
  [`502f74d`](https://github.com/Twingate/kubernetes-operator/commit/502f74d2d16856f115621e0b99131844bf15a44e))

- Bump black from 23.10.1 to 23.11.0
  ([#33](https://github.com/Twingate/kubernetes-operator/pull/33),
  [`28284ad`](https://github.com/Twingate/kubernetes-operator/commit/28284ad7ead047500e3b0381578b70f844c547e1))

- Bump black from 23.11.0 to 23.12.0
  ([#67](https://github.com/Twingate/kubernetes-operator/pull/67),
  [`1725941`](https://github.com/Twingate/kubernetes-operator/commit/1725941cd13c8d7d3368ad036a97ba9da5d334d9))

- Bump black from 23.12.0 to 23.12.1
  ([#80](https://github.com/Twingate/kubernetes-operator/pull/80),
  [`fb2bff3`](https://github.com/Twingate/kubernetes-operator/commit/fb2bff31c06e8f9c78b86f0ad034ec14def2302b))

- Bump gitpython from 3.1.37 to 3.1.41
  ([#88](https://github.com/Twingate/kubernetes-operator/pull/88),
  [`cf03bb0`](https://github.com/Twingate/kubernetes-operator/commit/cf03bb0457b541b4b900941da40e3a3bdfe0fe52))

- Bump golang.org/x/crypto from 0.14.0 to 0.17.0
  ([#74](https://github.com/Twingate/kubernetes-operator/pull/74),
  [`33d5f7e`](https://github.com/Twingate/kubernetes-operator/commit/33d5f7edd403808bcd98516c9d8693f1137f1bc3))

- Bump google-cloud-artifact-registry from 1.9.0 to 1.10.0
  ([#61](https://github.com/Twingate/kubernetes-operator/pull/61),
  [`2196492`](https://github.com/Twingate/kubernetes-operator/commit/21964921d81884aeca6468e02a5abda3d44c651d))

- Bump gql from 3.4.1 to 3.5.0 ([#83](https://github.com/Twingate/kubernetes-operator/pull/83),
  [`2134808`](https://github.com/Twingate/kubernetes-operator/commit/2134808d4eef1ddbda618eb04329166fee860a89))

- Bump isort from 5.12.0 to 5.13.0 ([#64](https://github.com/Twingate/kubernetes-operator/pull/64),
  [`36061f2`](https://github.com/Twingate/kubernetes-operator/commit/36061f2bfd7fb8887d1c188a380d6ceb65fa3e0d))

- Bump isort from 5.13.0 to 5.13.1 ([#66](https://github.com/Twingate/kubernetes-operator/pull/66),
  [`3611312`](https://github.com/Twingate/kubernetes-operator/commit/3611312a5644ea3f6ef91a2408e5990dcc3e9514))

- Bump isort from 5.13.1 to 5.13.2 ([#69](https://github.com/Twingate/kubernetes-operator/pull/69),
  [`5515058`](https://github.com/Twingate/kubernetes-operator/commit/5515058c4db8cddd648a267632ef1fbed55e12db))

- Bump jinja2 from 3.1.2 to 3.1.3 ([#89](https://github.com/Twingate/kubernetes-operator/pull/89),
  [`290cbbb`](https://github.com/Twingate/kubernetes-operator/commit/290cbbba9cff2bf68aec0a1eef0301a87a45f133))

- Bump kubernetes from 28.1.0 to 29.0.0
  ([#86](https://github.com/Twingate/kubernetes-operator/pull/86),
  [`36af9e5`](https://github.com/Twingate/kubernetes-operator/commit/36af9e5bec36eba988f7400491f091dfb325e606))

- Bump mypy from 1.6.1 to 1.7.0 ([#37](https://github.com/Twingate/kubernetes-operator/pull/37),
  [`858efb0`](https://github.com/Twingate/kubernetes-operator/commit/858efb0452867e1e45e47595e5e72c63be71ab77))

- Bump mypy from 1.7.0 to 1.7.1 ([#51](https://github.com/Twingate/kubernetes-operator/pull/51),
  [`2da6a12`](https://github.com/Twingate/kubernetes-operator/commit/2da6a1220a1978f81d41cd70113d4b17b0b426c3))

- Bump mypy from 1.7.1 to 1.8.0 ([#77](https://github.com/Twingate/kubernetes-operator/pull/77),
  [`3a7fd5d`](https://github.com/Twingate/kubernetes-operator/commit/3a7fd5df943fe1ed43d88ee790341d79e0f38d75))

- Bump pendulum from 2.1.2 to 3.0.0 ([#73](https://github.com/Twingate/kubernetes-operator/pull/73),
  [`982e747`](https://github.com/Twingate/kubernetes-operator/commit/982e747272168476d04d4658809096c05d95af9f))

- Bump pre-commit from 3.5.0 to 3.6.0
  ([#63](https://github.com/Twingate/kubernetes-operator/pull/63),
  [`3eb9d07`](https://github.com/Twingate/kubernetes-operator/commit/3eb9d0757aad13bb376e7366859ec46c74984713))

- Bump pydantic from 2.4.2 to 2.5.0 ([#43](https://github.com/Twingate/kubernetes-operator/pull/43),
  [`c2dddfb`](https://github.com/Twingate/kubernetes-operator/commit/c2dddfb048b4cfee7f392bc50284b60bd1f92970))

- Bump pydantic from 2.5.0 to 2.5.1 ([#47](https://github.com/Twingate/kubernetes-operator/pull/47),
  [`b2a9df5`](https://github.com/Twingate/kubernetes-operator/commit/b2a9df5f413cbce69cef192dc9db3fd5e91463d2))

- Bump pydantic from 2.5.1 to 2.5.2 ([#50](https://github.com/Twingate/kubernetes-operator/pull/50),
  [`132983d`](https://github.com/Twingate/kubernetes-operator/commit/132983dd171d8e1ed6794a16b76053c843bcdc2b))

- Bump pydantic from 2.5.2 to 2.5.3 ([#76](https://github.com/Twingate/kubernetes-operator/pull/76),
  [`f994717`](https://github.com/Twingate/kubernetes-operator/commit/f994717041bef4947836e5690e38126dcf972163))

- Bump pydantic-settings from 2.0.3 to 2.1.0
  ([#44](https://github.com/Twingate/kubernetes-operator/pull/44),
  [`71b4c11`](https://github.com/Twingate/kubernetes-operator/commit/71b4c116e68a795c1c9974c298f011156c9e0c4a))

- Bump pytest from 7.4.3 to 7.4.4 ([#81](https://github.com/Twingate/kubernetes-operator/pull/81),
  [`3a2c181`](https://github.com/Twingate/kubernetes-operator/commit/3a2c181ff9ea69db821159197a14591c43c3a6e8))

- Bump python-semantic-release from 8.3.0 to 8.5.0
  ([#60](https://github.com/Twingate/kubernetes-operator/pull/60),
  [`973f0de`](https://github.com/Twingate/kubernetes-operator/commit/973f0de3cbddb3170640b3ac8ac0c2db6ddcdcf0))

- Bump python-semantic-release from 8.5.0 to 8.5.1
  ([#68](https://github.com/Twingate/kubernetes-operator/pull/68),
  [`eec07cb`](https://github.com/Twingate/kubernetes-operator/commit/eec07cb860f0ed046b78f70355b91942655f9c0c))

- Bump python-semantic-release from 8.5.1 to 8.5.2
  ([#75](https://github.com/Twingate/kubernetes-operator/pull/75),
  [`1ce66db`](https://github.com/Twingate/kubernetes-operator/commit/1ce66db7ed428d9591188e178528a91d444ba6d8))

- Bump python-semantic-release from 8.5.2 to 8.7.0
  ([#78](https://github.com/Twingate/kubernetes-operator/pull/78),
  [`15daa70`](https://github.com/Twingate/kubernetes-operator/commit/15daa702e9620fd4121ec859ab7f397958f1e756))

- Bump responses from 0.23.3 to 0.24.0
  ([#29](https://github.com/Twingate/kubernetes-operator/pull/29),
  [`79e169a`](https://github.com/Twingate/kubernetes-operator/commit/79e169a3e8c4d392eb3e1a0352e2c0bafba3ca66))

- Bump responses from 0.24.0 to 0.24.1
  ([#46](https://github.com/Twingate/kubernetes-operator/pull/46),
  [`b9e62a2`](https://github.com/Twingate/kubernetes-operator/commit/b9e62a206c904fb82eca7723ebf6432695dbefee))

- Bump ruff from 0.1.11 to 0.1.12 ([#90](https://github.com/Twingate/kubernetes-operator/pull/90),
  [`e81271b`](https://github.com/Twingate/kubernetes-operator/commit/e81271bbcf3f12bfbf9bac29b186367520ca5ffb))

- Bump ruff from 0.1.12 to 0.1.13 ([#91](https://github.com/Twingate/kubernetes-operator/pull/91),
  [`35b23ad`](https://github.com/Twingate/kubernetes-operator/commit/35b23ade45cf80ceb82e20a9c82987cd8035b8f1))

- Bump ruff from 0.1.3 to 0.1.4 ([#31](https://github.com/Twingate/kubernetes-operator/pull/31),
  [`d218bfe`](https://github.com/Twingate/kubernetes-operator/commit/d218bfe2683a133e1b52bd1878066cdda66ac06f))

- Bump ruff from 0.1.4 to 0.1.5 ([#34](https://github.com/Twingate/kubernetes-operator/pull/34),
  [`363f50a`](https://github.com/Twingate/kubernetes-operator/commit/363f50a5899b3949602a4a0db2179333698bf9cb))

- Bump ruff from 0.1.5 to 0.1.6 ([#49](https://github.com/Twingate/kubernetes-operator/pull/49),
  [`74042b6`](https://github.com/Twingate/kubernetes-operator/commit/74042b67176454e434a134659ac1781fba70a2a5))

- Bump ruff from 0.1.6 to 0.1.7 ([#59](https://github.com/Twingate/kubernetes-operator/pull/59),
  [`64fe08d`](https://github.com/Twingate/kubernetes-operator/commit/64fe08d6d35031656cd1ecfb384cf4ea9d94940a))

- Bump ruff from 0.1.7 to 0.1.8 ([#70](https://github.com/Twingate/kubernetes-operator/pull/70),
  [`af3370c`](https://github.com/Twingate/kubernetes-operator/commit/af3370c3c6ac1360b96039a0a3b2e89c728b1160))

- Bump ruff from 0.1.8 to 0.1.9 ([#79](https://github.com/Twingate/kubernetes-operator/pull/79),
  [`b22629d`](https://github.com/Twingate/kubernetes-operator/commit/b22629ddcbe876b8c3b39701108ccc83d57e0dc5))

- Bump ruff from 0.1.9 to 0.1.11 ([#82](https://github.com/Twingate/kubernetes-operator/pull/82),
  [`6d3083c`](https://github.com/Twingate/kubernetes-operator/commit/6d3083cf6f81280cc968ecffc343bc0cce7e0208))

- Bump types-croniter from 2.0.0.0 to 2.0.0.20240106
  ([#85](https://github.com/Twingate/kubernetes-operator/pull/85),
  [`c247fd7`](https://github.com/Twingate/kubernetes-operator/commit/c247fd79bf46196f3e33e8beb5de9b8be3cc70ad))

- Bump types-requests from 2.31.0.6 to 2.31.0.20240106
  ([#87](https://github.com/Twingate/kubernetes-operator/pull/87),
  [`5739c52`](https://github.com/Twingate/kubernetes-operator/commit/5739c52b3b51588736bb376c08ae8d1211860d01))

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

- TwingateConnector object (auto provision and update)
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


## v0.1.1 (2023-10-30)

### Bug Fixes

- ResourceAccessSpec.get_resource_ref_object fetching wrong version
  ([#20](https://github.com/Twingate/kubernetes-operator/pull/20),
  [`86b6557`](https://github.com/Twingate/kubernetes-operator/commit/86b6557107ea927ec0244ba91ccacb680aab9751))


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

- Bump orjson from 3.9.9 to 3.9.10 ([#9](https://github.com/Twingate/kubernetes-operator/pull/9),
  [`298cccb`](https://github.com/Twingate/kubernetes-operator/commit/298cccbfa866ac39d090a77f1524d7aedd8e1e1d))

- Bump pytest from 7.4.2 to 7.4.3 ([#7](https://github.com/Twingate/kubernetes-operator/pull/7),
  [`089ce2b`](https://github.com/Twingate/kubernetes-operator/commit/089ce2b6ae94a710e65d8af1d6d9aeb9951f7ec7))

- Bump python-semantic-release from 8.1.2 to 8.3.0
  ([#10](https://github.com/Twingate/kubernetes-operator/pull/10),
  [`70b3a0c`](https://github.com/Twingate/kubernetes-operator/commit/70b3a0c18a2a752111026c0c8d58cca0b0a0fc97))

- Bump ruff from 0.1.1 to 0.1.3 ([#8](https://github.com/Twingate/kubernetes-operator/pull/8),
  [`e1524de`](https://github.com/Twingate/kubernetes-operator/commit/e1524de8dbdbc6f8f305b21c63da08cc632f3b72))

- Bump syrupy from 4.5.0 to 4.6.0 ([#11](https://github.com/Twingate/kubernetes-operator/pull/11),
  [`5e5b1f0`](https://github.com/Twingate/kubernetes-operator/commit/5e5b1f0ff55f4546a08d50742088afb4c498d543))

### Documentation

- README overhaul ([#15](https://github.com/Twingate/kubernetes-operator/pull/15),
  [`3c8e29c`](https://github.com/Twingate/kubernetes-operator/commit/3c8e29c309b2b5f6a7621db3e8842f703d5fb83e))

### Features

- Initial operator ([#1](https://github.com/Twingate/kubernetes-operator/pull/1),
  [`0bc53a8`](https://github.com/Twingate/kubernetes-operator/commit/0bc53a8ae9f3ed39486adbf7f57b4bf3774aff87))

- Support protocol restrictions on twingateresource
  ([#16](https://github.com/Twingate/kubernetes-operator/pull/16),
  [`0c95107`](https://github.com/Twingate/kubernetes-operator/commit/0c95107414e14d1624caf1e30b1acf5335a2a01c))


## v0.0.1 (2023-10-20)

- Initial Release
