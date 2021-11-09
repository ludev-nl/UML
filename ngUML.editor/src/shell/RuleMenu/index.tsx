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

    async function addRuleToDatabase(ruleString: string) {
         const data = new FormData();
         data.append("rule", ruleString)
         const json = await fetch("http://localhost:8000/rules/add/", 
                     {method: 'POST',
                     mode: "cors",
                     body: data
                 } )
                 .then(response => {
                         return response.json();
                 })
                 .catch(error => {
                     console.error('Error: ', error);
                 });
        return json
    }

    function databaseToRules() {
        var apiRules: string[] = []
        fetch("http://localhost:8000/rules/",
            {
                method: 'GET',
                mode: "cors",
            })
            .then(response => {
                return response.json();
            })
            .then(response => {
                for (var rule of response) {
                    apiRules.push(rule.fields["messy_rule"])
                }
                var rules = rulesStringState
                for (let apiRule of apiRules) {
                    rules.push(apiRule)
                }
                setRulesStringState(rules)
                rulesToComponents()
            })
            .catch(error => {
                console.error('Error: ', error);
            });
    }

    async function addRule(textArea: string){
        let textAreaObject = document.getElementById(textArea) as HTMLInputElement
        let valueOfTextArea = textAreaObject.value
        var ruleAdded = await addRuleToDatabase(valueOfTextArea)
        var badrule = document.getElementById("BadRules")
        if (ruleAdded.FAIL == null) {
            console.log("succes")
            badrule?.classList.remove("BadRulesShown")
            addToRules(valueOfTextArea)
        }
        else {
            console.log("fail")
            badrule?.classList.add("BadRulesShown")
        }
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
                    databaseToRules()
                }}
            >
                Get rules from database
            </Button>
            <Button
                onClick={() => { addRuleToDatabase("warehouse capacity < 50")} }
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