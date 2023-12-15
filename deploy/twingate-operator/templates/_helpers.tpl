{{/*
Expand the name of the chart.
*/}}
{{- define "twingate-operator.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "twingate-operator.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "twingate-operator.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "twingate-operator.labels" -}}
helm.sh/chart: {{ include "twingate-operator.chart" . }}
{{ include "twingate-operator.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "twingate-operator.selectorLabels" -}}
app.kubernetes.io/name: {{ include "twingate-operator.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "twingate-operator.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "twingate-operator.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "twingate-operator" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Get the Secret object name
*/}}
{{- define "twingate-operator.secretName" -}}
{{- if .Values.twingateOperator.existingAPIKeySecret -}}
{{- printf "%s" (tpl .Values.twingateOperator.existingAPIKeySecret.name $) -}}
{{- else -}}
{{- default (include "twingate-operator.fullname" .) -}}
{{- end -}}

{{/*
Get the Secret object apikey key
*/}}
{{- define "twingate-operator.secretApiKey" -}}
{{- if .Values.twingateOperator.existingAPIKeySecret -}}
{{- printf "%s" (tpl .Values.twingateOperator.existingAPIKeySecret.key $) -}}
{{- else -}}
{{- printf "TWINGATE_API_KEY" -}}
{{- end -}}
