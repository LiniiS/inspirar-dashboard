"""
Sistema de traduções para o Dashboard Inspirar
Suporta Português (pt) e Inglês (en)
"""

TRANSLATIONS = {
    'pt': {
        'dashboard': {
            'title': 'Dashboard Insights Avançados - Usuários do app Inspirar',
            'subtitle': 'Visualize, explore e compare dados de pacientes de forma interativa.',
            'upload_file': 'Carregue o arquivo JSON de pacientes',
            'total_patients': 'Total de pacientes analisados',
            'accounts_from': 'contas criadas a partir de março de 2025',
            'period_extraction': 'Período de Extração dos Dados',
            'period': 'Período',
            'data_extracted': 'Dados extraídos de 01/03/2025 a 06/02/2026',
            'info': 'Dashboard personalizado para análise de dados de pacientes usuários do app Inspirar',
            'contact': 'Dúvidas, sugestões, críticas, elogios: aline.dev@proton.me',
            'no_file': 'Faça upload do arquivo JSON para visualizar os insights.',
            'error_processing': 'Erro ao processar o arquivo JSON: {error}\n\nVerifique se o arquivo segue o formato correto. Consulte o exemplo em data/README.md.',
            'tabs': {
                'overview': '📊 Visão Geral',
                'demographics': '👥 Demografia',
                'medications': '💊 Medicamentos',
                'diaries': '📝 Diários & Atividades',
                'advanced': '📈 Análises Avançadas',
                'details': '📋 Dados Detalhados'
            },
            'tab_titles': {
                'overview': 'Visão Geral dos Pacientes',
                'demographics': 'Análise Demográfica',
                'medications': 'Medicamentos e Prescrições',
                'diaries': 'Diários e Atividades Físicas',
                'advanced': 'Análises Avançadas',
                'details': 'Dados Detalhados'
            }
        },
        'sections': {
            'metrics': {
                'title': 'Métricas Principais',
                'description': 'Indicadores quantitativos principais da amostra de pacientes no período selecionado.',
                'total_registered': 'Total cadastrados',
                'with_medication': 'Com medicamento (%)',
                'physical_activity': 'Atividade física (%)',
                'average_age': 'Idade média'
            },
            'ativos': {
                'title': 'Distribuição de Pacientes Ativos vs Inativos',
                'description': 'Mostra a proporção de pacientes que utilizaram pelo menos uma funcionalidade versus os inativos.',
                'note_personal_data': '**Nota sobre dados pessoais:** Pacientes que solicitaram exclusão de conta e dados pessoais têm seus dados de saúde mantidos para fins médicos, mas todos os dados pessoais (incluindo sexo) são removidos. Nestes casos, o sexo é registrado como "INDEFINIDO (I)" e estes pacientes não são representados no gráfico de distribuição por sexo dos pacientes ativos.',
                'active': 'Ativo',
                'inactive': 'Inativo',
                'distribution_title': 'Distribuição de Pacientes Ativos vs Inativos',
                'distribution_by_sex': 'Distribuição por Sexo - Pacientes Ativos',
                'total_active': 'Total de pacientes ativos',
                'active_by_sex': 'Ativos por sexo',
                'male': 'Masculino',
                'female': 'Feminino',
                'no_active_sex': 'Nenhum paciente ativo com sexo definido disponível para análise.',
                'no_active': 'Nenhum paciente ativo disponível para análise de distribuição por sexo.'
            },
            'status_acq': {
                'title': 'Status de Controle da Asma (ACQ) - Primeira Semana',
                'description': 'Análise do ACQ (Asthma Control Questionnaire) considerando apenas a **primeira conclusão temporal** de cada paciente (ordenada por data de criação/resposta). Isso fornece uma visão mais precisa do controle inicial da asma, garantindo consistência para análise médica.',
                'title_no_data': 'Status de Controle da Asma (ACQ)',
                'no_data': 'Nenhum registro de ACQ encontrado para a primeira semana de pacientes no período selecionado.',
                'engagement_metrics': 'Métricas de Engajamento ACQ',
                'total_patients': 'Total de Pacientes',
                'with_acq': 'Com ACQ',
                'without_acq': 'Sem ACQ',
                'completion_rate': 'Taxa de Preenchimento',
                'statistics_description': 'Estas estatísticas resumem a condição asmática registrada no **primeiro questionário ACQ** completado por cada paciente, na **primeira semana após a criação da conta**. Elas refletem o estado inicial do controle da asma, antes de quaisquer efeitos de acompanhamento.',
                'mean': 'Média',
                'std_deviation': 'Desvio Padrão',
                'median': 'Mediana',
                'iqr': 'IQR (25%-75%)',
                'visualizations': 'Visualizações - Primeira Semana',
                'scores_distribution': 'Distribuição de Scores ACQ',
                'control_status': 'Status de Controle da Asma',
                'patient_details': 'Detalhes dos Pacientes - Primeiro ACQ',
                'patient_details_info': 'Tabela com detalhes da primeira conclusão de ACQ de cada paciente, incluindo idade, sexo, data, score e status de controle.',
                'table_filters': 'Filtros da Tabela',
                'status': 'Status',
                'sex': 'Sexo',
                'min_score': 'Score Mínimo',
                'max_score': 'Score Máximo',
                'all': 'Todos',
                'filtered_patients': 'Pacientes filtrados: {filtered} de {total}',
                'total_with_valid_acq': 'Total de pacientes com ACQ válido na tabela: {total}',
                'download_table': '📥 Baixar Tabela (CSV)',
                'download_help': 'Baixar tabela com detalhes do primeiro ACQ de cada paciente'
            },
            'idade': {
                'title': 'Análise de Idade dos Pacientes',
                'description': 'Análise da faixa etária dos pacientes cadastrados, incluindo distribuição geral e por sexo.',
                'general_distribution': 'Distribuição Geral de Idade',
                'distribution_by_sex': 'Distribuição de Idade por Sexo',
                'statistics_by_sex': 'Estatísticas por Sexo',
                'total': 'Total',
                'mean': 'Média',
                'median': 'Mediana',
                'min_max': 'Faixa',
                'years': 'anos',
                'patients': 'pacientes',
                'no_data': 'Nenhum dado de idade disponível para análise.',
                'no_data_sex': 'Nenhum dado de idade com sexo definido disponível para análise.',
                'note_undefined': '**Nota:** {count} paciente(s) com sexo indefinido não aparecem no gráfico por sexo devido à política de exclusão de dados pessoais.'
            },
            'crises': {
                'title': 'Análise de Crises de Asma',
                'description': 'Análise abrangente de crises de asma: períodos de duração, medicamentos utilizados durante crises e distribuição por sexo.',
                'total_crises': 'Total de Crises',
                'patients_with_crisis': 'Pacientes com Crisis',
                'incidence_rate': 'Taxa de Incidência',
                'average_crises_patient': 'Média de Crises/Paciente',
                'no_crisis_data': 'Nenhum dado de crise registrado no período analisado.',
                'unable_to_process': 'Não foi possível processar os dados de crise.',
                'distribution_by_duration': 'Distribuição de Crises por Duração',
                'duration_statistics': 'Estatísticas de Duração',
                'average_duration': 'Duração Média',
                'median': 'Mediana',
                'maximum_duration': 'Duração Máxima',
                'minimum_duration': 'Duração Mínima',
                'days': 'dias',
                'distribution_by_range': 'Distribuição por Faixa',
                'analysis_by_sex': 'Análise de Crises por Sexo',
                'statistics_by_sex': 'Estatísticas por Sexo',
                'crises': 'Crises',
                'average_duration_sex': 'Duração média',
                'patients': 'Pacientes',
                'comparison': 'Comparação',
                'note_undefined': '**Nota:** {count} crise(s) de pacientes com sexo indefinido não aparecem na análise por sexo devido à política de exclusão de dados pessoais.',
                'no_crisis_sex': 'Nenhum dado de crise com sexo definido disponível para análise comparativa.',
                'detailed_data': 'Dados Detalhados de Crises',
                'undefined': 'Indefinido',
                'download_complete': '📥 Baixar Dados Completos (CSV)',
                'duration_ranges': {
                    '1_2': '1-2 dias',
                    '3_5': '3-5 dias',
                    '6_10': '6-10 dias',
                    '11_15': '11-15 dias',
                    '16_30': '16-30 dias',
                    'more_30': 'Mais de 30 dias'
                }
            },
            'diarios_semanais': {
                'title': 'Registros de Diários de Sintomas por Semana',
                'description': 'Esta seção mostra o comportamento semanal de registros de diários de sintomas: a análise considera apenas pacientes com contas criadas a partir de março de 2025.',
                'average_records': 'Média de Registros por Semana',
                'active_users_evolution': 'Evolução de Usuários Ativos por Período',
                'data_by_period': 'Dados por Período - Diários de Sintomas',
                'total_periods': 'Total de períodos analisados',
                'overall_average': 'Média geral de registros',
                'peak_active_users': 'Pico de usuários ativos',
                'download_csv': '📥 Baixar Dados por Período (CSV)',
                'no_data': 'Nenhum dado de diários encontrado para o período selecionado.'
            },
            'atividades_semanais': {
                'title': 'Registros de Atividade Física por Semana',
                'description': 'Esta seção mostra o comportamento semanal de registros de atividade física: a análise considera apenas pacientes com contas criadas a partir de março de 2025.',
                'average_records': 'Média de Registros por Semana',
                'total_steps': 'Total de Passos por Semana',
                'active_users_evolution': 'Evolução de Usuários Ativos por Período',
                'no_weeks': 'Nenhuma semana com usuários ativos para exibir no gráfico.',
                'individual_analysis': 'Análise Individual de Passos Diários',
                'select_patient': 'Selecione um paciente',
                'select_month': 'Selecione um mês',
                'detailed_daily_data': 'Dados Diários Detalhados',
                'no_activity_patient': 'Nenhuma atividade registrada para o paciente {patient} em {month}.',
                'no_patient_found': 'Nenhum paciente encontrado com ID válido.',
                'data_by_period': 'Dados por Período - Atividades Físicas',
                'total_periods': 'Total de períodos analisados',
                'overall_average': 'Média geral de registros',
                'peak_active_users': 'Pico de usuários ativos',
                'highest_steps': 'Maior total de passos em uma semana',
                'download_csv': '📥 Baixar Dados por Período (CSV)',
                'no_data': 'Nenhum dado de atividades encontrado para o período selecionado.'
            },
            'funcionalidades_geral': {
                'title': 'Visão Geral de Funcionalidades',
                'description': 'Visão geral global do uso de funcionalidades do app por pacientes.',
                'distribution_title': 'Distribuição do Número de Funcionalidades Utilizadas por Paciente',
                'distribution_info': 'Para cada paciente, conta quantas funcionalidades diferentes ele utilizou pelo menos uma vez (diário de sintomas, ACQ, atividade física, prescrição, crise). O gráfico mostra a distribuição desta contagem entre todos os pacientes.',
                'usage_statistics': 'Estatísticas de Uso',
                'average_features': 'Média de Funcionalidades',
                'median': 'Mediana',
                'mode_most_common': 'Moda (mais comum)',
                'distribution': 'Distribuição',
                'features': 'funcionalidades',
                'patients': 'pacientes',
                'general_summary': 'Resumo Geral',
                'active': 'Ativos',
                'inactive': 'Inativos',
                'activation_rate': 'Taxa de Ativação',
                'most_used_title': 'Ranking de Funcionalidades Mais Utilizadas',
                'most_used_info': 'Para cada funcionalidade, conta o número de pacientes que a utilizaram pelo menos uma vez no período analisado. O gráfico mostra o ranking das funcionalidades mais acessadas.',
                'feature_names': {
                    'diaries': 'Diários',
                    'acq': 'ACQ',
                    'activities': 'Atividades',
                    'prescriptions': 'Medicamentos',
                    'crises': 'Crises'
                },
                'number_of_features': 'Número de Funcionalidades',
                'number_of_patients': 'Número de Pacientes',
                'usage_count': 'Contagem de Uso',
                'percentage': 'Percentual'
            },
            'funcionalidades_sexo': {
                'title': 'Análise de Funcionalidades por Sexo',
                'description': 'Análise comparativa do uso de funcionalidades entre pacientes masculinos e femininos para identificar padrões de adesão por sexo.',
                'detailed_data': 'Dados Detalhados por Sexo',
                'summary': 'Resumo',
                'total_male': 'Total Masculino',
                'total_female': 'Total Feminino',
                'largest_difference': 'Maior diferença',
                'higher_adoption': 'Maior adesão',
                'difference': 'Diferença',
                'download_csv': '📥 Baixar Dados por Sexo (CSV)',
                'note_undefined': '**Nota:** {count} paciente(s) com sexo indefinido não aparecem nesta análise devido à política de exclusão de dados pessoais.',
                'no_data_sex': 'Nenhum dado com sexo definido disponível para análise comparativa.',
                'adoption_rate': 'Taxa de Adesão',
                'number_of_users': 'Número de Usuários'
            },
            'prescricoes_semanais': {
                'title': 'Prescrições e Administrações Semanais',
                'description': 'Esta seção mostra o comportamento semanal de uso de medicamentos: a análise considera apenas pacientes com contas criadas a partir de março de 2025.',
                'tab_administrations': '📊 Administrações por Semana',
                'tab_prescriptions': '📋 Prescrições por Semana',
                'admin_title': 'Total de Administrações (Tomadas de Medicamento) por Semana',
                'admin_info': 'Esta análise conta cada **administração** (tomada de medicamento) que ocorreu em cada período semanal.',
                'presc_title': 'Total de Prescrições Criadas por Semana',
                'presc_info': 'Esta análise conta cada **prescrição** que foi **criada** em cada período semanal.',
                'data_by_period': 'Dados por Período',
                'total_periods': 'Total de períodos',
                'total_administrations': 'Total de administrações',
                'peak_admin_week': 'Pico de administrações/semana',
                'peak_active_users': 'Pico de usuários ativos',
                'download_admin': '📥 Baixar Dados de Administrações (CSV)',
                'detailed_admin_title': '📋 Dados Detalhados de Administrações por Semana',
                'detailed_admin_info': 'Baixar tabela completa com todas as administrações agrupadas por semana e paciente para validação manual.',
                'total_admin_records': 'Total de registros de administrações',
                'showing_first': 'Mostrando primeiras {count} linhas de {total} registros totais. Baixe a tabela completa abaixo.',
                'download_detailed_admin': '📥 Baixar Tabela Completa de Administrações (CSV)',
                'no_admin_data': 'Nenhum dado de administrações encontrado.',
                'download_presc': '📥 Baixar Dados de Prescrições (CSV)',
                'detailed_presc_title': '📋 Dados Detalhados de Prescrições por Semana',
                'detailed_presc_info': 'Baixar tabela completa com todas as prescrições agrupadas por semana e paciente para validação manual.',
                'total_presc_records': 'Total de registros de prescrições',
                'download_detailed_presc': '📥 Baixar Tabela Completa de Prescrições (CSV)',
                'no_presc_data': 'Nenhum dado de prescrições encontrado.',
                'validation_title': '📋 Tabela Completa de Validação de Prescrições',
                'validation_info': 'Extração completa de todas as prescrições com seu status de tomada para validação de dados.',
                'total_presc_validation': 'Total de prescrições na tabela de validação',
                'download_validation': '📥 Baixar Tabela de Validação Completa (CSV)',
                'no_presc_validation': 'Nenhuma prescrição encontrada para tabela de validação.',
                'total_prescriptions': 'Total de Prescrições',
                'prescriptions_taken': 'Prescrições Tomadas',
                'prescriptions_not_taken': 'Prescrições Não Tomadas'
            },
            'tabelas': {
                'title': 'Tabelas Detalhadas com Filtro por Idade',
                'description': 'Tabela detalhada de pacientes, filtrável por faixa etária.',
                'age_range': 'Faixa Etária'
            },
            'recordes': {
                'title': 'Recordes e Destaques',
                'description': 'Destaques individuais, como paciente mais ativo baseado na média diária de passos.',
                'most_active': 'Paciente Mais Ativo',
                'id': 'ID',
                'account_created': 'Conta criada em',
                'analyzed_period': 'Período analisado',
                'days': 'dias',
                'total_steps': 'Total de passos',
                'daily_average': 'Média diária',
                'steps_per_day': 'passos/dia',
                'no_patient': 'Nenhum paciente com registros de atividade física encontrado',
                'general_statistics': 'Estatísticas Gerais',
                'active_patients': 'Pacientes ativos',
                'average_steps': 'Média de passos',
                'total_steps_all': 'Total de passos',
                'median': 'Mediana',
                'no_data': 'Nenhum dado de atividade física encontrado'
            },
            'barplot_metricas': {
                'title': 'Análise Descritiva e Distribuição de Métricas Numéricas',
                'select_metric': 'Selecione a métrica para análise',
                'mean': 'Média',
                'std_deviation': 'Desvio Padrão',
                'median': 'Mediana',
                'iqr': 'IQR (25%-75%)',
                'percentage_distribution': 'Distribuição Percentual de {metric}',
                'range': 'Faixa',
                'count': 'Quantidade',
                'percentage': 'Percentual',
                'detailed_table': 'Tabela Detalhada',
                'no_data': 'Nenhum dado disponível para a métrica selecionada.'
            },
            'mapa_calor': {
                'title': 'Mapa de Calor: Correlação entre Uso de Funcionalidades',
                'description': 'Para cada paciente, verifica se ele utilizou (1) ou não (0) cada funcionalidade pelo menos uma vez. A matriz de correlação mostra o quanto o uso de uma funcionalidade está associado ao uso de outras.',
                'comparative_analysis': 'Análise comparativa de correlações entre funcionalidades: visão geral e por sexo.',
                'general_correlation': 'Correlação Geral',
                'correlation_male': 'Correlação - Masculino',
                'correlation_female': 'Correlação - Feminino',
                'all_patients': 'Todos os Pacientes ({count} pacientes)',
                'male_patients': 'Pacientes Masculinos ({count} pacientes)',
                'female_patients': 'Pacientes Femininos ({count} pacientes)',
                'insufficient_data': 'Dados insuficientes para correlação (menos de 2 pacientes {sex})',
                'comparative_analysis_title': 'Análise Comparativa de Correlações',
                'strongest_correlations': 'Correlações Mais Fortes por Grupo',
                'correlation_summary': 'Resumo de Correlações',
                'group': 'Grupo',
                'strongest_correlation': 'Correlação Mais Forte',
                'value': 'Valor',
                'download_correlations': '📥 Baixar Correlações (CSV)',
                'insights': 'Insights',
                'insight_1': 'Valores próximos de **1**: funcionalidades usadas juntas',
                'insight_2': 'Valores próximos de **0**: uso independente',
                'insight_3': 'Valores próximos de **-1**: uso mutuamente exclusivo',
                'insufficient_comparative': 'Dados insuficientes para análise comparativa por sexo.',
                'note_undefined': '**Nota:** {count} paciente(s) com sexo indefinido não aparecem na análise por sexo devido à política de exclusão de dados pessoais.',
                'general_view': 'Visão Geral',
                'by_sex': 'Por Sexo',
                'correlation': 'Correlação',
                'general': 'Geral',
                'male': 'Masculino',
                'female': 'Feminino'
            }
        },
        'charts': {
            'labels': {
                'acq_score': 'Score ACQ',
                'age': 'Idade',
                'period': 'Período',
                'number_of_crises': 'Número de Crises',
                'duration': 'Duração',
                'duration_range': 'Faixa de Duração',
                'average_records': 'Média de Registros',
                'active_users': 'Usuários Ativos',
                'total_steps': 'Total de Passos',
                'week': 'Semana'
            },
            'titles': {
                'acq_scores_distribution': 'Distribuição de Scores ACQ',
                'control_status': 'Status de Controle da Asma',
                'crises_by_duration': 'Número de Crises por Faixa de Duração',
                'crises_by_sex_duration': 'Distribuição de Crises por Sexo e Duração',
                'diaries_by_week': 'Registros de Diários por Semana',
                'activities_by_week': 'Registros de Atividades por Semana',
                'steps_by_week': 'Total de Passos por Semana',
                'features_distribution': 'Distribuição do Número de Funcionalidades Utilizadas',
                'most_used_features': 'Ranking de Funcionalidades Mais Utilizadas',
                'adoption_rate_by_sex': 'Taxa de Adesão por Sexo (%)',
                'users_by_feature_sex': 'Número de Usuários por Funcionalidade e Sexo'
            }
        },
        'tables': {
            'patient_id': 'ID do Paciente',
            'age': 'Idade',
            'sex': 'Sexo',
            'first_acq_date': 'Data do Primeiro ACQ',
            'acq_score': 'Score ACQ',
            'status': 'Status',
            'total_acqs': 'Total de ACQs',
            'height': 'Altura (m)',
            'weight': 'Peso (kg)',
            'total_diaries': 'Total Diários',
            'total_acqs_table': 'Total ACQs',
            'total_activities': 'Total Atividades',
            'total_medications': 'Total Medicamentos',
            'total_crises': 'Total Crises',
            'duration_days': 'Duração (dias)',
            'start_date': 'Data de Início',
            'end_date': 'Data de Fim',
            'duration_range': 'Faixa de Duração',
            'period': 'Período',
            'average_records': 'Média de Registros',
            'active_users': 'Usuários Ativos',
            'total_steps': 'Total de Passos'
        }
    },
    'en': {
        'dashboard': {
            'title': 'Dashboard Insights Avançados - Usuários do app Inspirar',
            'subtitle': 'Visualize, explore and compare patient data interactively.',
            'upload_file': 'Upload patient JSON file',
            'total_patients': 'Total patients analyzed',
            'accounts_from': 'accounts created from March 2025 onwards',
            'period_extraction': 'Data Extraction Period',
            'period': 'Period',
            'data_extracted': 'Data extracted from 01/03/2025 to 06/02/2026',
            'info': 'Customized dashboard for analyzing patient data from Inspirar app users',
            'contact': 'Questions, suggestions, criticism, praise: aline.dev@proton.me',
            'no_file': 'Upload the JSON file to view insights.',
            'error_processing': 'Error processing JSON file: {error}\n\nCheck if the file follows the correct format. See example in data/README.md.',
            'tabs': {
                'overview': '📊 Overview',
                'demographics': '👥 Demographics',
                'medications': '💊 Medications',
                'diaries': '📝 Diaries & Activities',
                'advanced': '📈 Advanced Analysis',
                'details': '📋 Detailed Data'
            },
            'tab_titles': {
                'overview': 'Patient Overview',
                'demographics': 'Demographic Analysis',
                'medications': 'Medications and Prescriptions',
                'diaries': 'Diaries and Physical Activities',
                'advanced': 'Advanced Analysis',
                'details': 'Detailed Data'
            }
        },
        'sections': {
            'metrics': {
                'title': 'Main Metrics',
                'description': 'Main quantitative indicators of the patient sample in the selected period.',
                'total_registered': 'Total registered',
                'with_medication': 'With medication (%)',
                'physical_activity': 'Physical activity (%)',
                'average_age': 'Average age'
            },
            'ativos': {
                'title': 'Active vs Inactive Patients Distribution',
                'description': 'Shows the proportion of patients who used at least one feature versus inactive ones.',
                'note_personal_data': '**Note on personal data:** Patients who requested account and personal data deletion have their health data kept for medical purposes, but all personal data (including sex) is removed. In these cases, sex is recorded as "UNDEFINED (I)" and these patients are not represented in the sex distribution chart of active users.',
                'active': 'Active',
                'inactive': 'Inactive',
                'distribution_title': 'Active vs Inactive Patients Distribution',
                'distribution_by_sex': 'Distribution by Sex - Active Patients',
                'total_active': 'Total active patients',
                'active_by_sex': 'Active by sex',
                'male': 'Male',
                'female': 'Female',
                'no_active_sex': 'No active patients with defined sex available for analysis.',
                'no_active': 'No active patients available for sex distribution analysis.'
            },
            'status_acq': {
                'title': 'Asthma Control Status (ACQ) - First Week',
                'description': 'Analysis of ACQ (Asthma Control Questionnaire) considering only the **first temporal completion** of each patient (ordered by creation/answer date). This provides a more accurate view of initial asthma control, ensuring consistency for medical analysis.',
                'title_no_data': 'Asthma Control Status (ACQ)',
                'no_data': 'No ACQ records found for the first week of patients in the selected period.',
                'engagement_metrics': 'ACQ Engagement Metrics',
                'total_patients': 'Total Patients',
                'with_acq': 'With ACQ',
                'without_acq': 'Without ACQ',
                'completion_rate': 'Completion Rate',
                'statistics_description': 'These statistics summarize the asthmatic condition recorded in the **first ACQ questionnaire** completed by each patient, in the **first week after account creation**. They reflect the initial state of asthma control, before any follow-up effects.',
                'mean': 'Mean',
                'std_deviation': 'Std Deviation',
                'median': 'Median',
                'iqr': 'IQR (25%-75%)',
                'visualizations': 'Visualizations - First Week',
                'scores_distribution': 'ACQ Scores Distribution',
                'control_status': 'Asthma Control Status',
                'patient_details': 'Patient Details - First ACQ',
                'patient_details_info': 'Table with details of the first ACQ completion of each patient, including age, sex, date, score and control status.',
                'table_filters': 'Table Filters',
                'status': 'Status',
                'sex': 'Sex',
                'min_score': 'Min Score',
                'max_score': 'Max Score',
                'all': 'All',
                'filtered_patients': 'Filtered patients: {filtered} of {total}',
                'total_with_valid_acq': 'Total patients with valid ACQ in table: {total}',
                'download_table': '📥 Download Table (CSV)',
                'download_help': 'Download table with details of the first ACQ of each patient'
            },
            'idade': {
                'title': 'Age Distribution Analysis',
                'description': 'Analysis of registered patients age range, including general and sex-based distribution.',
                'general_distribution': 'General Age Distribution',
                'distribution_by_sex': 'Age Distribution by Sex',
                'statistics_by_sex': 'Statistics by Sex',
                'total': 'Total',
                'mean': 'Mean',
                'median': 'Median',
                'min_max': 'Range',
                'years': 'years',
                'patients': 'patients',
                'no_data': 'No age data available for analysis.',
                'no_data_sex': 'No age data with defined sex available for analysis.',
                'note_undefined': '**Note:** {count} patient(s) with undefined sex do not appear in the sex chart due to personal data exclusion policy.'
            },
            'crises': {
                'title': 'Asthma Crisis Analysis',
                'description': 'Comprehensive analysis of asthma crises: duration periods, medications used during crises, and distribution by sex.',
                'total_crises': 'Total Crises',
                'patients_with_crisis': 'Patients with Crisis',
                'incidence_rate': 'Incidence Rate',
                'average_crises_patient': 'Average Crises/Patient',
                'no_crisis_data': 'No crisis data recorded in the analyzed period.',
                'unable_to_process': 'Unable to process crisis data.',
                'distribution_by_duration': 'Crisis Distribution by Duration',
                'duration_statistics': 'Duration Statistics',
                'average_duration': 'Average Duration',
                'median': 'Median',
                'maximum_duration': 'Maximum Duration',
                'minimum_duration': 'Minimum Duration',
                'days': 'days',
                'distribution_by_range': 'Distribution by Range',
                'analysis_by_sex': 'Crisis Analysis by Sex',
                'statistics_by_sex': 'Statistics by Sex',
                'crises': 'Crises',
                'average_duration_sex': 'Average duration',
                'patients': 'Patients',
                'comparison': 'Comparison',
                'note_undefined': '**Note:** {count} crisis(es) from patients with undefined sex do not appear in the sex analysis due to personal data exclusion policy.',
                'no_crisis_sex': 'No crisis data with defined sex available for comparative analysis.',
                'detailed_data': 'Detailed Crisis Data',
                'undefined': 'Undefined',
                'download_complete': '📥 Download Complete Data (CSV)',
                'duration_ranges': {
                    '1_2': '1-2 days',
                    '3_5': '3-5 days',
                    '6_10': '6-10 days',
                    '11_15': '11-15 days',
                    '16_30': '16-30 days',
                    'more_30': 'More than 30 days'
                }
            },
            'diarios_semanais': {
                'title': 'Symptom Diary Records by Week',
                'description': 'This section shows weekly symptom diary record behavior: analysis considers only patients with accounts created from March 2025 onwards.',
                'average_records': 'Average Records per Week',
                'active_users_evolution': 'Active Users Evolution by Period',
                'data_by_period': 'Data by Period - Symptom Diaries',
                'total_periods': 'Total periods analyzed',
                'overall_average': 'Overall average records',
                'peak_active_users': 'Peak active users',
                'download_csv': '📥 Download Data by Period (CSV)',
                'no_data': 'No diary data found for the selected period.'
            },
            'atividades_semanais': {
                'title': 'Physical Activity Records by Week',
                'description': 'This section shows weekly physical activity record behavior: analysis considers only patients with accounts created from March 2025 onwards.',
                'average_records': 'Average Records per Week',
                'total_steps': 'Total Steps per Week',
                'active_users_evolution': 'Active Users Evolution by Period',
                'no_weeks': 'No weeks with active users to display in chart.',
                'individual_analysis': 'Individual Daily Steps Analysis',
                'select_patient': 'Select a patient',
                'select_month': 'Select a month',
                'detailed_daily_data': 'Detailed Daily Data',
                'no_activity_patient': 'No activity recorded for patient {patient} in {month}.',
                'no_patient_found': 'No patient found with valid ID.',
                'data_by_period': 'Data by Period - Physical Activities',
                'total_periods': 'Total periods analyzed',
                'overall_average': 'Overall average records',
                'peak_active_users': 'Peak active users',
                'highest_steps': 'Highest total steps in a week',
                'download_csv': '📥 Download Data by Period (CSV)',
                'no_data': 'No activity data found for the selected period.'
            },
            'funcionalidades_geral': {
                'title': 'Global Feature Usage Overview',
                'description': 'Global overview of app feature usage by patients.',
                'distribution_title': 'Distribution of Number of Features Used per Patient',
                'distribution_info': 'For each patient, it counts how many different features they used at least once (symptom diary, ACQ, physical activity, prescription, crisis). The chart shows the distribution of this count among all patients.',
                'usage_statistics': 'Usage Statistics',
                'average_features': 'Average Features',
                'median': 'Median',
                'mode_most_common': 'Mode (most common)',
                'distribution': 'Distribution',
                'features': 'features',
                'patients': 'patients',
                'general_summary': 'General Summary',
                'active': 'Active',
                'inactive': 'Inactive',
                'activation_rate': 'Activation Rate',
                'most_used_title': 'Most Used Features Ranking',
                'most_used_info': 'For each feature, it counts the number of patients who used it at least once in the analyzed period. The chart shows the ranking of the most accessed features.',
                'feature_names': {
                    'diaries': 'Diaries',
                    'acq': 'ACQ',
                    'activities': 'Activities',
                    'prescriptions': 'Medications',
                    'crises': 'Crises'
                },
                'number_of_features': 'Number of Features',
                'number_of_patients': 'Number of Patients',
                'usage_count': 'Usage Count',
                'percentage': 'Percentage'
            },
            'funcionalidades_sexo': {
                'title': 'Feature Usage Analysis by Sex',
                'description': 'Comparative analysis of feature usage between male and female patients to identify adoption patterns by sex.',
                'detailed_data': 'Detailed Data by Sex',
                'summary': 'Summary',
                'total_male': 'Total Male',
                'total_female': 'Total Female',
                'largest_difference': 'Largest difference',
                'higher_adoption': 'Higher adoption',
                'difference': 'Difference',
                'download_csv': '📥 Download Data by Sex (CSV)',
                'note_undefined': '**Note:** {count} patient(s) with undefined sex do not appear in this analysis due to personal data exclusion policy.',
                'no_data_sex': 'No data with defined sex available for comparative analysis.',
                'adoption_rate': 'Adoption Rate',
                'number_of_users': 'Number of Users'
            },
            'prescricoes_semanais': {
                'title': 'Weekly Prescriptions and Administrations',
                'description': 'This section shows weekly medication intake behavior: analysis considers only patients with accounts created from March 2025 onwards.',
                'tab_administrations': '📊 Administrations by Week',
                'tab_prescriptions': '📋 Prescriptions by Week',
                'admin_title': 'Total Administrations (Medication Intakes) by Week',
                'admin_info': 'This analysis counts each **administration** (medication intake) that occurred in each week period.',
                'presc_title': 'Total Prescriptions Created by Week',
                'presc_info': 'This analysis counts each **prescription** that was **created** in each week period.',
                'data_by_period': 'Data by Period',
                'total_periods': 'Total periods',
                'total_administrations': 'Total administrations',
                'peak_admin_week': 'Peak administrations/week',
                'peak_active_users': 'Peak active users',
                'download_admin': '📥 Download Administrations Data (CSV)',
                'detailed_admin_title': '📋 Detailed Administrations Data by Week',
                'detailed_admin_info': 'Download complete table with all administrations grouped by week and patient for manual validation.',
                'total_admin_records': 'Total administrations records',
                'showing_first': 'Showing first {count} rows of {total} total records. Download full table below.',
                'download_detailed_admin': '📥 Download Complete Administrations Table (CSV)',
                'no_admin_data': 'No administrations data found.',
                'download_presc': '📥 Download Prescriptions Data (CSV)',
                'detailed_presc_title': '📋 Detailed Prescriptions Data by Week',
                'detailed_presc_info': 'Download complete table with all prescriptions grouped by week and patient for manual validation.',
                'total_presc_records': 'Total prescriptions records',
                'download_detailed_presc': '📥 Download Complete Prescriptions Table (CSV)',
                'no_presc_data': 'No prescriptions data found.',
                'validation_title': '📋 Complete Prescription Validation Table',
                'validation_info': 'Complete extraction of all prescriptions with their taken status for data validation.',
                'total_presc_validation': 'Total prescriptions in validation table',
                'download_validation': '📥 Download Complete Validation Table (CSV)',
                'no_presc_validation': 'No prescriptions found for validation table.',
                'total_prescriptions': 'Total Prescriptions',
                'prescriptions_taken': 'Prescriptions Taken',
                'prescriptions_not_taken': 'Prescriptions Not Taken'
            },
            'tabelas': {
                'title': 'Detailed Tables with Age Filter',
                'description': 'Detailed patient table, filterable by age range.',
                'age_range': 'Age Range'
            },
            'recordes': {
                'title': 'Records and Highlights',
                'description': 'Individual highlights, such as most active patient based on daily average steps.',
                'most_active': 'Most Active Patient',
                'id': 'ID',
                'account_created': 'Account created on',
                'analyzed_period': 'Analyzed period',
                'days': 'days',
                'total_steps': 'Total steps',
                'daily_average': 'Daily average',
                'steps_per_day': 'steps/day',
                'no_patient': '📊 No patient with physical activity records found',
                'general_statistics': '📊 General Statistics',
                'active_patients': 'Active patients',
                'average_steps': 'Average steps',
                'total_steps_all': 'Total steps (all)',
                'median': 'Median',
                'no_data': '📊 No physical activity data found'
            },
            'barplot_metricas': {
                'title': 'Descriptive Analysis and Distribution of Numerical Metrics',
                'select_metric': 'Select metric for analysis',
                'mean': 'Mean',
                'std_deviation': 'Std Deviation',
                'median': 'Median',
                'iqr': 'IQR (25%-75%)',
                'percentage_distribution': 'Percentage Distribution of {metric}',
                'range': 'Range',
                'count': 'Count',
                'percentage': 'Percentage',
                'detailed_table': 'Detailed Table',
                'no_data': 'No data available for the selected metric.'
            },
            'mapa_calor': {
                'title': 'Heatmap: Correlation between Feature Usage',
                'description': 'For each patient, it checks if they used (1) or not (0) each feature at least once. The correlation matrix shows how much the use of one feature is associated with the use of others.',
                'comparative_analysis': 'Comparative analysis of correlations between features: general view and by sex.',
                'general_correlation': 'General Correlation',
                'correlation_male': 'Correlation - Male',
                'correlation_female': 'Correlation - Female',
                'all_patients': 'All Patients ({count} patients)',
                'male_patients': 'Male Patients ({count} patients)',
                'female_patients': 'Female Patients ({count} patients)',
                'insufficient_data': 'Insufficient data for correlation (less than 2 {sex} patients)',
                'comparative_analysis_title': 'Comparative Correlation Analysis',
                'strongest_correlations': 'Strongest Correlations by Group',
                'correlation_summary': 'Correlation Summary',
                'group': 'Group',
                'strongest_correlation': 'Strongest Correlation',
                'value': 'Value',
                'download_correlations': '📥 Download Correlations (CSV)',
                'insights': 'Insights',
                'insight_1': 'Values close to **1**: features used together',
                'insight_2': 'Values close to **0**: independent use',
                'insight_3': 'Values close to **-1**: mutually exclusive use',
                'insufficient_comparative': 'Insufficient data for comparative analysis by sex.',
                'note_undefined': '**Note:** {count} patient(s) with undefined sex do not appear in the sex analysis due to personal data exclusion policy.',
                'general_view': 'General View',
                'by_sex': 'By Sex',
                'correlation': 'Correlation',
                'general': 'General',
                'male': 'Male',
                'female': 'Female'
            }
        },
        'charts': {
            'labels': {
                'acq_score': 'ACQ Score',
                'age': 'Age',
                'period': 'Period',
                'number_of_crises': 'Number of Crises',
                'duration': 'Duration',
                'duration_range': 'Duration Range',
                'average_records': 'Average Records',
                'active_users': 'Active Users',
                'total_steps': 'Total Steps',
                'week': 'Week'
            },
            'titles': {
                'acq_scores_distribution': 'ACQ Scores Distribution',
                'control_status': 'Asthma Control Status',
                'crises_by_duration': 'Number of Crises by Duration Range',
                'crises_by_sex_duration': 'Crisis Distribution by Sex and Duration',
                'diaries_by_week': 'Symptom Diary Records by Week',
                'activities_by_week': 'Physical Activity Records by Week',
                'steps_by_week': 'Total Steps per Week',
                'features_distribution': 'Distribution of Number of Features Used',
                'most_used_features': 'Most Used Features Ranking',
                'adoption_rate_by_sex': 'Feature Adoption Rate by Sex (%)',
                'users_by_feature_sex': 'Number of Users by Feature and Sex'
            }
        },
        'tables': {
            'patient_id': 'Patient ID',
            'age': 'Age',
            'sex': 'Sex',
            'first_acq_date': 'First ACQ Date',
            'acq_score': 'ACQ Score',
            'status': 'Status',
            'total_acqs': 'Total ACQs',
            'height': 'Height (m)',
            'weight': 'Weight (kg)',
            'total_diaries': 'Total Diaries',
            'total_acqs_table': 'Total ACQs',
            'total_activities': 'Total Activities',
            'total_medications': 'Total Medications',
            'total_crises': 'Total Crises',
            'duration_days': 'Duration (days)',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'duration_range': 'Duration Range',
            'period': 'Period',
            'average_records': 'Average Records',
            'active_users': 'Active Users',
            'total_steps': 'Total Steps'
        }
    }
}


def get_translation(key: str, lang: str = None) -> str:
    """
    Obtém tradução para a chave especificada.
    
    Args:
        key: Chave de tradução no formato 'categoria.subcategoria.chave' (ex: 'dashboard.title')
        lang: Idioma ('pt' ou 'en'). Se None, usa o idioma do session_state.
    
    Returns:
        String traduzida ou a própria chave se não encontrar tradução.
    """
    import streamlit as st
    
    if lang is None:
        lang = st.session_state.get('language', 'pt')
    
    # Fallback para inglês se idioma não suportado
    if lang not in TRANSLATIONS:
        lang = 'en'
    
    keys = key.split('.')
    translation = TRANSLATIONS[lang]
    
    try:
        for k in keys:
            translation = translation[k]
        
        # Se chegou aqui, encontrou a tradução
        return translation
    except (KeyError, TypeError):
        # Se não encontrar, retorna a chave original
        return key


def t(key: str, **kwargs) -> str:
    """
    Função helper para obter traduções com suporte a formatação.
    
    Args:
        key: Chave de tradução
        **kwargs: Argumentos para formatação (ex: t('key', count=5))
    
    Returns:
        String traduzida e formatada.
    """
    translation = get_translation(key)
    
    # Se houver kwargs, tenta formatar a string
    if kwargs:
        try:
            return translation.format(**kwargs)
        except (KeyError, ValueError):
            # Se falhar na formatação, retorna sem formatar
            return translation
    
    return translation

