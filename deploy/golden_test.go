package golden

import (
    "flag"
    "fmt"
    "os"
    "path/filepath"
    "regexp"
    "strings"
    "testing"

    "github.com/gruntwork-io/terratest/modules/helm"
    "gopkg.in/yaml.v2"
)

var update = flag.Bool("update", false, "update golden test output files")

type ChartYaml struct {
    Name    string `yaml:"name"`
    Version string `yaml:"version"`
}

func GetChartYaml(t *testing.T) ChartYaml {
    chartYamlFile, err := os.ReadFile("./twingate-operator/Chart.yaml")
    if err != nil {
        t.Fatalf("Error reading Chart.yaml: %v", err)
    }

    var chartYaml ChartYaml

    if err := yaml.Unmarshal(chartYamlFile, &chartYaml); err != nil {
        t.Fatalf("Error unmarshaling YAML data: %v", err)
    }

    return chartYaml
}

func TestHelmRender(t *testing.T) {
    files, err := os.ReadDir("./test/golden")
    if err != nil {
        t.Fatal(err)
    }

    chartYaml := GetChartYaml(t)

    for _, f := range files {
        if !f.IsDir() && strings.HasSuffix(f.Name(), ".yaml") && !strings.HasSuffix(f.Name(), ".golden.yaml") {
            // Render this values.yaml file
            output, error := helm.RenderTemplateE(t,
                &helm.Options{
                    ValuesFiles: []string{"test/golden/" + f.Name()},
                },
                "./twingate-operator",
                "test",
                []string{},
            )

            goldenFile := "test/golden/" + strings.TrimSuffix(f.Name(), filepath.Ext(".yaml")) + ".golden.yaml"

            if error != nil {
                output = fmt.Sprintf("%v\n", error)
            } else {
                // Replace `cn.chart` helper value with a stable value for testing
                regex := regexp.MustCompile(fmt.Sprintf("%s-%s", chartYaml.Name, chartYaml.Version))
                bytes := regex.ReplaceAll([]byte(output), []byte(fmt.Sprintf("%s-major.minor.patch-test", chartYaml.Name)))
                output = fmt.Sprintf("%s\n", string(bytes))
            }

            if *update {
                err := os.WriteFile(goldenFile, []byte(output), 0644)
                if err != nil {
                    t.Fatal(err)
                }
            }

            expected, err := os.ReadFile(goldenFile)
            if err != nil {
                t.Fatal(err)
            }

            if string(expected) != output {
                t.Fatalf("Expected %s, but got %s\n. Update golden files by running `go test -v ./... -update`", string(expected), output)
            }
        }

    }
}
