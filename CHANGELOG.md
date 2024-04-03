# CHANGELOG



## v0.8.0 (2024-04-03)

### Chore

* chore: Add more Ruff linters (#233) ([`7f918be`](https://github.com/Twingate/kubernetes-operator/commit/7f918be0983adad30747bad5c53a561dbf6b25fe))

### Feature

* feat: Add TwingateConnector sidecarContainers prop (#234) ([`835da7c`](https://github.com/Twingate/kubernetes-operator/commit/835da7cc3848c8040096d41938f5d36926ad1618))


## v0.7.0 (2024-03-26)

### Feature

* feat: TwingateConnector - allow defining extra pod annotations with `podAnnotations` (#225) ([`7b44838`](https://github.com/Twingate/kubernetes-operator/commit/7b44838f8ade8cfcabe79669d32e83a0c31ab9ca))

* feat: twingateresourceaccess - allow specifying principal by name (#62) ([`0b1e69b`](https://github.com/Twingate/kubernetes-operator/commit/0b1e69b14fb2006ff0e30af5d23567b5e718d4f9))

* feat: Make TwingateConnector&#39;s containerExtra and podExtra mutable (#223) ([`e7d8425`](https://github.com/Twingate/kubernetes-operator/commit/e7d84255a64bfd77e5a9f7749471a03cebaeccf6))

### Fix

* fix: Add validation for TwingateConnector when provider is “google” (#224) ([`68e188e`](https://github.com/Twingate/kubernetes-operator/commit/68e188ed769822640160a92148a05b0dfbdd41b6))


## v0.6.3 (2024-03-25)

### Chore

* chore: Upgrade Go to 1.22.0 and setup dependabot (#205) ([`6f53ebf`](https://github.com/Twingate/kubernetes-operator/commit/6f53ebf45a52a76b6fb35b8d190a51bf827e6c2d))

* chore: Temporary disable poetry package-mode until dependabot upgrades ([`7b4c207`](https://github.com/Twingate/kubernetes-operator/commit/7b4c20730574983b2e08fddc71a0ca6105e3bb9c))

* chore: Integration test for old pod migration (#190) ([`2dff2b3`](https://github.com/Twingate/kubernetes-operator/commit/2dff2b36c960bddaa3e448a94ed68415a8ef4cb9))

### Fix

* fix: Allow env to be defined in containerExtra (#222) ([`14f5ef5`](https://github.com/Twingate/kubernetes-operator/commit/14f5ef5fd14cfee09cd4669ac8b20cb250ee550d))


## v0.6.2 (2024-03-11)

### Fix

* fix: Resource restricted policy should allow empty ports (#193) ([`e9aec7d`](https://github.com/Twingate/kubernetes-operator/commit/e9aec7d9ee7be6944d4c69b8d9d73107d3a38df5))


## v0.6.1 (2024-03-07)

### Chore

* chore: Set poetry to package-mode = false (#188) ([`f91f57a`](https://github.com/Twingate/kubernetes-operator/commit/f91f57a17905d648041b0099dc5568700440a121))

### Fix

* fix: Fix k8s_force_delete_pod finalizers removal (#189) ([`5b2a8f3`](https://github.com/Twingate/kubernetes-operator/commit/5b2a8f396a7abbacf958c37406b2c4dd6dc6bd6a))


## v0.6.0 (2024-03-06)

### Chore

* chore: Upgrade Poetry to latest 1.8.2 (#183) ([`128de82`](https://github.com/Twingate/kubernetes-operator/commit/128de8227d303e47dbf127f64aaef9114439bee1))

* chore: Upgrade Poetry to 1.8.1 (#181) ([`2f490f8`](https://github.com/Twingate/kubernetes-operator/commit/2f490f8e833bb32d50eabd8f5d5df198f174e812))

### Feature

* feat: Improved TwingateConnector reconciliation (#180) ([`e0a4f25`](https://github.com/Twingate/kubernetes-operator/commit/e0a4f25c14f706de4e6149e302d61e41d6515a68))

### Fix

* fix: Connector pod updates &#34;Forbidden&#34; error (#184) ([`8096e62`](https://github.com/Twingate/kubernetes-operator/commit/8096e62c89d238035653f9e57ded8ece028505f6))


## v0.5.0 (2024-03-01)

### Chore

* chore: Pydantic deprecated .dict() for .model_dump() (#171) ([`065c146`](https://github.com/Twingate/kubernetes-operator/commit/065c14687389e0de66575709d5b05e6403f55e39))

* chore: Switch from Black to Ruff Formatter (#148) ([`1b822ae`](https://github.com/Twingate/kubernetes-operator/commit/1b822ae23be0cc7ec0cc4b5dffccf52c332dd696))

* chore: Stalebot is deprecated. Move to actions/stale@v9 (#147) ([`94dce35`](https://github.com/Twingate/kubernetes-operator/commit/94dce35289d97e1c2674c3530d7418fe870b55e1))

### Feature

* feat: Add `hasStatusNotificationsEnabled` to `TwingateConnector` (#170) ([`f03f851`](https://github.com/Twingate/kubernetes-operator/commit/f03f851bdc1b9cf7f59e618205a5c3ae3baf55f5))

### Fix

* fix: Improved `twingate_connector_recreate_pod` logic (#179) ([`fd3f533`](https://github.com/Twingate/kubernetes-operator/commit/fd3f533dfc2d4a67a8679dd2666c249f0869f500))

* fix: LABEL_CONNECTOR_POD_DELETED isnt set to false after pod recreated (#177) ([`f3d6865`](https://github.com/Twingate/kubernetes-operator/commit/f3d686599e43a175c10d3a8032187d47e74e61dd))

* fix: Reduce update scope for `twingate_resource_update` (#176) ([`c947fba`](https://github.com/Twingate/kubernetes-operator/commit/c947fba876047317f2921e0bbb52654fded66e38))

* fix: Limit twingate_resource_access_update scope to spec (#175) ([`75ff3f0`](https://github.com/Twingate/kubernetes-operator/commit/75ff3f05a0159dff0d3f454141baf546cbc0eb1f))

* fix: Add status and logs to `twingate_connector_resume` (#168) ([`13495f0`](https://github.com/Twingate/kubernetes-operator/commit/13495f0ade55b07728accde0080b34f6bbe84877))

* fix: twingate connector doesnt handle pod deletion on resume (#162) ([`7fbc24b`](https://github.com/Twingate/kubernetes-operator/commit/7fbc24b0d41a5b47dc397851c10911aac94bb777))

* fix: Deleting an item already deleted on Twingate Admin should not fail (#160) ([`3cd447f`](https://github.com/Twingate/kubernetes-operator/commit/3cd447f1caa07772b8d821c34d96de88c159724d))

### Unknown

* Upgrade local tooling for 3.11.8 ([`4cdaec0`](https://github.com/Twingate/kubernetes-operator/commit/4cdaec0658de1c7da7a6f490fed34a2bc3fd9156))


## v0.4.0 (2024-02-15)

### Chore

* chore: Upgrade Poetry to 1.7.1 (#144) ([`fd18505`](https://github.com/Twingate/kubernetes-operator/commit/fd18505a98047a4e65b8bbc0eb24f0520f7d1462))

* chore: Monitor and update github actions ([`98f48f9`](https://github.com/Twingate/kubernetes-operator/commit/98f48f9b6c5aa1aaa2a67edc8815775b2d527de3))

### Feature

* feat: Add podLabels (#129) ([`642af6a`](https://github.com/Twingate/kubernetes-operator/commit/642af6a1bb87f696ff07557ab78de63eefa40b82))

* feat: Add support for priorityClassName (#128) ([`e2d233c`](https://github.com/Twingate/kubernetes-operator/commit/e2d233c86569ec38ce905f1d8e244fff94090b60))

### Fix

* fix: Fix resource `protocols` diffing and serialization (#146) ([`7c9407e`](https://github.com/Twingate/kubernetes-operator/commit/7c9407e52185129201cf79a7bf5d6551711a16f9))

* fix: Disable healthcheck access logs (#135) ([`ad8eaba`](https://github.com/Twingate/kubernetes-operator/commit/ad8eabac03313d60959f9dc9ac48308a5114fa82))

* fix: Added `twingate_connector_image_update` to handle `image` updates (#131) ([`25f2753`](https://github.com/Twingate/kubernetes-operator/commit/25f27537eb292b632163978a16c23b3053b0e637))


## v0.3.0 (2024-01-30)

### Build

* build: Make CHANGELOG generation nicer (#98) ([`c13b35b`](https://github.com/Twingate/kubernetes-operator/commit/c13b35bca740a24df2dcf510ba09fcf1bd62d1b5))

### Feature

* feat: Add relevant security context to run as non root (#103) ([`c1cdfb7`](https://github.com/Twingate/kubernetes-operator/commit/c1cdfb7c664aff1f15ea274e8f12a7c945811b33))

* feat: Add seccompProfile by default (#104) ([`e3ef8d6`](https://github.com/Twingate/kubernetes-operator/commit/e3ef8d6ad9350ccdf95dcf3eb022ed73e845c530))


## v0.2.0 (2024-01-18)

### Build

* build: Replace pydocstyle with ruff (#35) ([`b771c7a`](https://github.com/Twingate/kubernetes-operator/commit/b771c7a659525f9414964606189ec4ff2dd2384e))

### Chore

* chore: Sort lines on pyproject dependencies (#39) ([`62c1338`](https://github.com/Twingate/kubernetes-operator/commit/62c133801a9f744988e80ca939815f642bc0c6d1))

* chore: adding the docker vulnerability monitor (#30)

Co-authored-by: Eran Kampf &lt;eran@ekampf.com&gt;
Co-authored-by: Eran Kampf &lt;205185+ekampf@users.noreply.github.com&gt; ([`b9af2ec`](https://github.com/Twingate/kubernetes-operator/commit/b9af2ecb4189d466c19b6fd86c104380e182b201))

### Documentation

* docs: Add descriptions to CRD fields (#48) ([`bdd6110`](https://github.com/Twingate/kubernetes-operator/commit/bdd6110c7a49a24d069090bc9a3927bc34bf3127))

### Feature

* feat: Add allowPrivilegeEscalation: false to values.yaml (#92) ([`55a4ce2`](https://github.com/Twingate/kubernetes-operator/commit/55a4ce2e7a15ceb74d64c2997f7943779430aed3))

* feat: Allow setting remote network by name (#84) ([`835c4c2`](https://github.com/Twingate/kubernetes-operator/commit/835c4c2bd55c07a602bfdbfff8854be47e4946bc))

* feat: Allow specifying API Key via reference to an external Secret (#72) ([`a028068`](https://github.com/Twingate/kubernetes-operator/commit/a0280684cf9d6302ba460e1f99d76e0dd15b8e32))

* feat: Allow customizing connector logLevel (#58) ([`b2323a8`](https://github.com/Twingate/kubernetes-operator/commit/b2323a845c71e2f3911b2a36e925345061740b24))

* feat: Add GCP Support for connector imagePolicy (#54) ([`0b5b84f`](https://github.com/Twingate/kubernetes-operator/commit/0b5b84f64999b1ced7a6a734ec8673319c0cf16d))

* feat: TwingateConnector object (auto provision and update) (#27) ([`7a135f2`](https://github.com/Twingate/kubernetes-operator/commit/7a135f26d2e4cb6bcbdf4839ac76f62149443f1f))

### Fix

* fix: gql.Client can&#39;t be singleton as its not thread-safe (#96) ([`f137124`](https://github.com/Twingate/kubernetes-operator/commit/f137124489e9705f6b7aba93714e3f90d31b8a04))

* fix: test_remote_network_name_gets_network_id (#97) ([`9c0afb9`](https://github.com/Twingate/kubernetes-operator/commit/9c0afb9167087b9037e6cec92c2d8d78a75bc3a1))

* fix: typo in class name - TwingateRety -&gt; TwingateRetry (#95) ([`a9d8882`](https://github.com/Twingate/kubernetes-operator/commit/a9d88827a72e95cd28d8026ffc38bbf5f942e370))

* fix: ClusterRole definition - create\delete pods and secrets required by Connector functionality (#94) ([`d4674fc`](https://github.com/Twingate/kubernetes-operator/commit/d4674fc8ae8e4a702806e1b63c6571abc4f6c936))

* fix: Allow setting remote network by name - TwingateSettings failure (#93) ([`a958588`](https://github.com/Twingate/kubernetes-operator/commit/a95858881bc18f7f4a3c46c333d2ca6351452520))

* fix: chore, build changes should change patch (#36) ([`cfda90b`](https://github.com/Twingate/kubernetes-operator/commit/cfda90bda4476f4d94d60755d6e522025660b545))

### Test

* test: remove unused fixture (#42) ([`6cd4d68`](https://github.com/Twingate/kubernetes-operator/commit/6cd4d68f924d051bbfec441ae31710a0e3b3dccb))

* test: Randomize test runs and fix errorsa (#41) ([`f953678`](https://github.com/Twingate/kubernetes-operator/commit/f953678a610f5dbc0d4b65016aebf02372f225e8))

* test: Use pytest-factoryboy instead of defining factory fixtures manually (#40) ([`8b3d012`](https://github.com/Twingate/kubernetes-operator/commit/8b3d0129a1cb4b403ea87d3dbb2ec2ca923c69b9))

* test: Simplify integration tests setup (#38) ([`d757085`](https://github.com/Twingate/kubernetes-operator/commit/d75708577a1d89e186fb08b4c887316d0b40fa56))

* test: Reorganize integration tests (#28) ([`86a27e4`](https://github.com/Twingate/kubernetes-operator/commit/86a27e46b24c975b0a13497d67107d0e3fd6c632))

### Unknown

* Update README.md ([`9693dc0`](https://github.com/Twingate/kubernetes-operator/commit/9693dc00c48c8344c9a432e99f4e75f7481e66ca))

* Fix: CVE-2023-5752 - always use latest pip (#56) ([`390b510`](https://github.com/Twingate/kubernetes-operator/commit/390b5100db009106ee1dd41cc3e52f2166f08d1f))

* Allow manually triggering CI ([`955228b`](https://github.com/Twingate/kubernetes-operator/commit/955228bd9352b0de8040b55f9552cdde81bb4de0))


## v0.1.2 (2023-11-01)

### Documentation

* docs: Improve development docs (#25) ([`ebf8cdb`](https://github.com/Twingate/kubernetes-operator/commit/ebf8cdbbcc368636e9af76c8c7ed24233c2bf378))

### Fix

* fix: change persistence layer - operator.twingate.com to just twingate.com (#24) ([`d7ebd7b`](https://github.com/Twingate/kubernetes-operator/commit/d7ebd7bf624182430671989587c2c767018180a7))

### Test

* test: resourceaccess integration testing (#23)

Co-authored-by: Eran Kampf &lt;eran@ekampf.com&gt; ([`8aa5621`](https://github.com/Twingate/kubernetes-operator/commit/8aa5621aa02f1efc0fef1dc49fb1624b3309ee4f))


## v0.1.1 (2023-10-30)

### Fix

* fix: ResourceAccessSpec.get_resource_ref_object fetching wrong version (#20)

Co-authored-by: semantic-release &lt;semantic-release&gt; ([`86b6557`](https://github.com/Twingate/kubernetes-operator/commit/86b6557107ea927ec0244ba91ccacb680aab9751))


## v0.1.0 (2023-10-30)

### Build

* build: Fix missing semantic-release dependency on release_dev step (#14) ([`e07e364`](https://github.com/Twingate/kubernetes-operator/commit/e07e364b858bf4a125ee103ce4c1e1e9e4f05c07))

### Chore

* chore: Add Issue Templates (#17) ([`b478434`](https://github.com/Twingate/kubernetes-operator/commit/b47843494d2e3e4549cad10d9814fead08a43353))

### Documentation

* docs: README overhaul (#15) ([`3c8e29c`](https://github.com/Twingate/kubernetes-operator/commit/3c8e29c309b2b5f6a7621db3e8842f703d5fb83e))

### Feature

* feat: Support protocol restrictions on twingateresource (#16) ([`0c95107`](https://github.com/Twingate/kubernetes-operator/commit/0c95107414e14d1624caf1e30b1acf5335a2a01c))

* feat: Initial operator (#1) ([`0bc53a8`](https://github.com/Twingate/kubernetes-operator/commit/0bc53a8ae9f3ed39486adbf7f57b4bf3774aff87))

### Fix

* fix: Change persistence settings to use Twingate namespace (#18) ([`41729d3`](https://github.com/Twingate/kubernetes-operator/commit/41729d342d95d00d6a1319e95ea8dfd4021a1228))

* fix: Fix helm chart + add log formatting  (#19) ([`9fb6675`](https://github.com/Twingate/kubernetes-operator/commit/9fb66755ecc6018d20e63988a305b1cbd0fb07b6))

* fix: Dev release tags (#13) ([`28ad640`](https://github.com/Twingate/kubernetes-operator/commit/28ad6407a388c35b2cc521f1a43497f9a244fb9c))


## v0.0.1 (2023-10-20)

### Unknown

* initial ([`50e4a88`](https://github.com/Twingate/kubernetes-operator/commit/50e4a888030eb8a56ee61ac13813cfae5cf6484a))
