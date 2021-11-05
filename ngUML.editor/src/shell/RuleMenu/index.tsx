import React, { useState } from 'react'
import './_rulemenu.css'
import {
    TextArea,
    Button,
    OrderedList,
    ListItem,
    Tooltip
} from 'carbon-components-react'
		
export const RuleMenu: React.FC = () => {
    const [rulesState, setRulesState] = useState<JSX.Element[]>([])
    const [rulesStringState, setRulesStringState] = useState<string[]>([])

    function apiToRules() {
        var apiRules: string[] = ["Rule een", "Rule twee"]
        var rules = rulesStringState
        for (let apiRule of apiRules) {
            rules.push(apiRule)
        }
        setRulesStringState(rules)
        rulesToComponents()
    }

    function addRule(textArea: string){
        let textAreaObject = document.getElementById(textArea) as HTMLInputElement
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
    }

    function addToRules(toAdd: string) {
        var rules = rulesStringState
        rules.push(toAdd)
        setRulesStringState(rules)
        rulesToComponents()
    }

    function deleteFromRules(toDelete: string){
        var rules = rulesStringState
        var index = 0
        for(let rule of rules){
            if (rule === toDelete){
                rules.splice(index, 1)
            }
            index++
        }
        setRulesStringState(rules)
        rulesToComponents()
    }

    function rulesToComponents() {
        var rulesComponents: JSX.Element[] = []
        for (let rule of rulesStringState) {
            let ruleComponent: JSX.Element = <ListItem key={rule}>{rule}
                <Tooltip className="tooltip">Do you want to edit or delete this rule?
                <Button onClick={() => {
                    deleteFromRules(rule)
                    addRule("editTextArea")
                    }}
                >Edit</Button><Button className="deleteButton" onClick={() => {deleteFromRules(rule)}}>Delete</Button>
                <TextArea
                    labelText=""
                    id="editTextArea"
                    defaultValue={rule}
                ></TextArea>
                </Tooltip></ListItem>
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
                onClick={() => {addRule("RuleTextArea")}}
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
            <Button
                onClick={async () => {
                    const response = fetch(
                        "http://127.0.0.1:8000/rules/",
                        {
                            method: 'GET',
                            mode: 'no-cors'
                        }
                    )

                    const response1 = fetch(
                        "http://127.0.0.1:8000/rules/add/",
                        {
                            method: 'POST',
                            mode: 'no-cors',
                            body: JSON.stringify({rule: 'warehouse storage > 50'})
                        }
                    )

                    console.log(await response1)
                }}
                id="populateButton"
            >
                Populate database
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