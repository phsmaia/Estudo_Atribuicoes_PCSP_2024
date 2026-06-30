import ast

def add_explanations():
    with open('explanations.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # We will just do a string replacement on the end of the dicts.
    
    new_tec_m3 = """
            "m3_macro_31": \"\"\"**📖 Compreensão Científica: Volume Total por Cenário**
    
Demonstra o quantitativo bruto de atribuições consolidadas em cada corte temporal.
- **Interpretação:** Verifica se as normativas, de modo geral, estão ampliando o escopo funcional da Polícia Civil ou enxugando as atribuições descritas.\"\"\",
            
            "m3_macro_32": \"\"\"**📖 Compreensão Científica: Proporção Exclusiva vs Compartilhada**

Avalia a relação percentual entre funções que pertencem a apenas um cargo e funções que pertencem a múltiplos cargos.
- **Interpretação:** Um ganho em atribuições exclusivas sugere uma especialização maior e isolamento de carreiras. Um aumento de compartilhadas indica generalismo e sobreposição legal.\"\"\",
            
            "m3_macro_33": \"\"\"**📖 Compreensão Científica: Grau Médio de Compartilhamento**

Mede, em média, por quantas carreiras distintas uma atribuição normativa é dividida.
- **Interpretação:** Valores altos demonstram alta capilaridade das funções (atribuições genéricas presentes em vários editais). Valores baixos indicam que as atribuições estão bem nichadas.\"\"\",
"""

    new_tec_m4 = """
            "m4_micro_inicio": \"\"\"**📖 Compreensão Científica: Rastreamento Evolutivo Individual**
            
Desagrega as métricas globais e projeta a variação pontual ao longo das 5 eras normativas para os cargos isolados.
- **Interpretação:** Analisa a variação da carreira em volume absoluto, conexões de adjacência, proximidade de Gower e saltos filogenéticos.\"\"\",

            "m4_micro_41": \"\"\"**📖 Compreensão Científica: Flutuação de Volume Funcional**
            
Série temporal da contagem absoluta de atribuições condensadas ativas no perfil da carreira.
- **Interpretação:** Evidencia crescimento (expansão legal do cargo) ou encolhimento (esvaziamento normativo).\"\"\",

            "m4_micro_42": \"\"\"**📖 Compreensão Científica: Dinâmica de Exclusividade**
            
Acompanha a proporção interna de atribuições exclusivas (privativas) versus compartilhadas.
- **Interpretação:** Revela se a carreira está perdendo o monopólio de suas funções (aumento de compartilhadas) ou ganhando nichos privativos.\"\"\",

            "m4_micro_43": \"\"\"**📖 Compreensão Científica: Densidade de Adjacência**
            
Soma das interseções brutas com todas as outras carreiras (Σ adjacências).
- **Interpretação:** Indica o quão "misturada" a carreira está. Picos sinalizam um aumento brusco de funções em comum com outros cargos.\"\"\",

            "m4_micro_44": \"\"\"**📖 Compreensão Científica: Centralidade de Grau (Degree)**
            
O número de arestas incidentes ao nó do cargo na malha de conectividade (limiar > 1).
- **Interpretação:** Mede o poder de conexão (hub). Crescimento sugere que a carreira interage com mais carreiras distintas do que antes.\"\"\",

            "m4_micro_45": \"\"\"**📖 Compreensão Científica: Distanciamento Gower (Isolamento)**
            
Média aritmética das distâncias de Gower em relação aos demais nós.
- **Interpretação:** Um vetor decrescente significa que o cargo está ficando estatisticamente mais genérico/parecido com o resto da corporação.\"\"\",

            "m4_micro_46": \"\"\"**📖 Compreensão Científica: Ruptura de Vizinhança**
            
Rastreia alterações na identidade do vizinho euclidiano mais próximo (menor distância Gower).
- **Interpretação:** Troca de vizinho representa um salto filogenético (Clado), sinalizando mudança radical no DNA funcional da carreira.\"\"\",
"""

    new_lei_m3 = """
            "m3_macro_31": \"\"\"**🗣️ Entendendo de forma simples: Crescimento Total**
            
Soma tudo o que a Polícia faz em cada época.
- **Como ler:** Subiu? A Polícia tem mais regras sobre o que fazer. Desceu? Enxugaram as atribuições nos editais.\"\"\",

            "m3_macro_32": \"\"\"**🗣️ Entendendo de forma simples: Exclusivas vs Compartilhadas**

Compara o que é de uma profissão só com o que "todo mundo faz".
- **Como ler:** Mais cor vermelha (exclusivas) significa que cada um está mais no seu quadrado. Mais azul (compartilhadas) significa que as carreiras estão atuando nas mesmas áreas.\"\"\",

            "m3_macro_33": \"\"\"**🗣️ Entendendo de forma simples: Média de Compartilhamento**

Em média, por quantas pessoas uma tarefa é dividida?
- **Como ler:** Se a média sobe, as tarefas estão cada vez mais diluídas entre vários cargos. Se desce, as funções estão mais específicas para cada profissão.\"\"\",
"""

    new_lei_m4 = """
            "m4_micro_inicio": \"\"\"**🗣️ Entendendo de forma simples: O Raio-X do Cargo no Tempo**

É o histórico de como a carreira mudou desde o primeiro edital até hoje.
- **Como ler:** Acompanhe a linha do seu cargo e veja se, com o passar dos anos, ele foi ganhando ou perdendo força, e se está ficando mais parecido ou diferente dos outros.\"\"\",

            "m4_micro_41": \"\"\"**🗣️ Entendendo de forma simples: Total de Funções**

A contagem básica de "quantas coisas" o cargo faz.
- **Como ler:** Linha subindo significa que o cargo ganhou novas responsabilidades na lei. Linha caindo significa esvaziamento.\"\"\",

            "m4_micro_42": \"\"\"**🗣️ Entendendo de forma simples: Privilégio vs Divisão**

Das coisas que o cargo faz, quantas são SÓ dele?
- **Como ler:** Se a barra de exclusivas diminui ao longo dos anos, significa que o cargo perdeu exclusividades e passou a dividir o trabalho com outros.\"\"\",

            "m4_micro_43": \"\"\"**🗣️ Entendendo de forma simples: Grau de Mistura**

Mede quantas tarefas no total o cargo divide com a corporação.
- **Como ler:** Crescimento indica que a carreira está cada vez mais justaposta e misturada com o trabalho alheio.\"\"\",

            "m4_micro_44": \"\"\"**🗣️ Entendendo de forma simples: Pontes de Conexão**

De 14 cargos, com quantos o seu cargo tem funções em comum?
- **Como ler:** Se antes ele dividia tarefas com 2 cargos e agora divide com 8, ele virou um "coringa" que atua em toda a delegacia.\"\"\",

            "m4_micro_45": \"\"\"**🗣️ Entendendo de forma simples: Isolamento da Profissão**

O quão "único" é o seu cargo comparado a todos os outros?
- **Como ler:** Linha subindo (perto de 1.0) significa que a carreira está se distanciando de todos e virando uma ilha (isolada). Linha descendo significa que está virando um "faz tudo" genérico.\"\"\",

            "m4_micro_46": \"\"\"**🗣️ Entendendo de forma simples: Troca de "Irmão Gêmeo"**

Quem é o cargo mais parecido com o seu?
- **Como ler:** Se o vizinho muda de uma década para outra, as alterações na lei foram tão pesadas que você literalmente mudou de família profissional.\"\"\",
"""

    # Replace end of tecnico dict
    content = content.replace('            "m4_micro": """**📖 Compreensão Científica: Rastreamento Evolutivo Individual (Séries Temporais)**\n\nDesagrega as métricas globais e projeta a variação pontual ao longo das 5 eras normativas para os cargos isolados.\n- **Interpretação:** Analisa o ganho/perda de volume funcional absoluto (total), a flutuação de distâncias magnéticas e os saltos de vizinhança topológica. Serve para rastrear a genealogia histórica individualizada."""\n        },', '            "m4_micro": """**📖 Compreensão Científica: Rastreamento Evolutivo Individual (Séries Temporais)**\n\nDesagrega as métricas globais e projeta a variação pontual ao longo das 5 eras normativas para os cargos isolados.\n- **Interpretação:** Analisa o ganho/perda de volume funcional absoluto (total), a flutuação de distâncias magnéticas e os saltos de vizinhança topológica. Serve para rastrear a genealogia histórica individualizada.""",\n' + new_tec_m3 + new_tec_m4 + '        },')

    # Replace end of leigo dict
    content = content.replace('            "m4_micro": """**🗣️ Entendendo de forma simples: Histórico Individual (Raio-X do Cargo)**\n\nÉ como a carteirinha de vacinação ou o boletim escolar do cargo ao longo do tempo.\n- **Como ler:** Você acompanha a mesma linha em todos os 5 cenários. Pode ver claramente se, ao longo das décadas, o cargo ganhou volume de trabalho (subiu) ou perdeu (desceu), e se ele se aproximou ou se afastou das outras profissões."""\n        }\n    }', '            "m4_micro": """**🗣️ Entendendo de forma simples: Histórico Individual (Raio-X do Cargo)**\n\nÉ como a carteirinha de vacinação ou o boletim escolar do cargo ao longo do tempo.\n- **Como ler:** Você acompanha a mesma linha em todos os 5 cenários. Pode ver claramente se, ao longo das décadas, o cargo ganhou volume de trabalho (subiu) ou perdeu (desceu), e se ele se aproximou ou se afastou das outras profissões.""",\n' + new_lei_m3 + new_lei_m4 + '        }\n    }')

    with open('explanations.py', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Sucesso!")

if __name__ == "__main__":
    add_explanations()
