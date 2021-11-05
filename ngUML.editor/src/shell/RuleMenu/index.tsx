import React, { useState} from 'react'
import './_rulemenu.css'
import {
    TextArea,
    Button,
    OrderedList,
    ListItem
} from 'carbon-components-react'

		
export const RuleMenu: React.FC = () => {
    const [rulesState, setRulesState] = useState<JSX.Element[]>([])
    const [rulesStringState, setRulesStringState] = useState<string[]>([])

    // API CALL EXAMPLE!
    //
    // function apiToRules() {
    //     // var apiRules: string[] = ["Rule een", "Rule twee"]
    //     // var rules = rulesStringState
    //     // for (let apiRule of apiRules) {
    //     //     rules.push(apiRule)
    //     // }
    //     // setRulesStringState(rules)
    //     // rulesToComponents()
    //     const data = new FormData();
    //     data.append("rule", "warehouse capacity < 50")
    //     fetch("http://localhost:8000/rules/add/", 
    //                 {method: 'POST',
    //                 mode: "cors",
    //                 body: data
    //             } )
    //             .then(response => {
    //                     return response.json();
    //             })
    //             .then(data => {
    //                 console.log('Success:', data);
    //             })
    //             .catch(error => {
    //                 console.error('Error: ', error);
    //             });
    // }
    
    function apiToRules() {
        var apiRules: string[] = ["Rule een", "Rule twee"]
        var rules = rulesStringState
        for (let apiRule of apiRules) {
            rules.push(apiRule)
        }
        setRulesStringState(rules)
        rulesToComponents()
    }

    function addToRules(toAdd: string) {
        var rules = rulesStringState
        rules.push(toAdd)
        setRulesStringState(rules)
        rulesToComponents()
    }

    function rulesToComponents() {
        var rulesComponents: JSX.Element[] = []
        for (let rule of rulesStringState) {
            let ruleComponent: JSX.Element = <ListItem key={rule}>{rule}</ListItem>
            rulesComponents.push(ruleComponent)
        }
        setRulesState(rulesComponents)
    }


    return (
        <div
            id="RuleMenu"
        >
        	<span 
        		id="Header"
        	>
        		Rules
            </span>
            <TextArea
                labelText=""
                placeholder="Write here your rule..."
                id="RuleTextArea"
            >
            </TextArea>
            <Button
                id="AddRuleButton"
                onClick={() => {
                    let textAreaObject = document.getElementById("RuleTextArea") as HTMLInputElement
                    let valueOfTextArea = textAreaObject.value
                    let badrule = document.getElementById("BadRules")
                    if (valueOfTextArea.includes("bad")) {
                        badrule?.classList.add("BadRulesShown")
                    }
                    else {
                        addToRules(valueOfTextArea)
                        badrule?.classList.remove("BadRulesShown")
                    }
                    console.log(valueOfTextArea)
                }}
            >
                Add rule
            </Button>
            <span
                id="BadRules"
            >
                You entered a bad rule!
            </span>
            <hr>
            </hr>
            <Button
                onClick={() => {
                    apiToRules()
                }}
            >
                Get rules from database
            </Button>
            <OrderedList
                id="ruleList"
            >
                {rulesState}
            </OrderedList>
        </div>
    )
}

export default RuleMenu