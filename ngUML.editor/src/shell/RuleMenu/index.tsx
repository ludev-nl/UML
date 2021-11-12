import React, { useState } from 'react'
import './_rulemenu.css'
import {
    TextArea,
    Button,
    OrderedList,
    ListItem,
    Tooltip
} from 'carbon-components-react'

class RuleObject {
    id: string
    messy_rule: string
    processed_rule: string
    type: string
    python: string

    constructor(id: string, messy_rule: string, processed_rule: string, type: string, python: string) {
        this.id = id
        this.messy_rule = messy_rule
        this.processed_rule = processed_rule
        this.type = type
        this.python = python
    }

    toString() {
        console.log("id: " + this.id + ", messy rule: " + this.messy_rule + ", processed rule: " + this.processed_rule + ", type: " + this.type + ", python: " + this.python)
    }
}
		
export const RuleMenu: React.FC = () => {
    const [rulesState, setRulesState] = useState<JSX.Element[]>([])
    const [rulesObject, setRulesObject] = useState<RuleObject[]>([])

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
        var apiRulesObject: RuleObject[] = []
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
                    var ruleObject: RuleObject = new RuleObject(rule.pk, rule.fields["messy_rule"], rule.fields["processed_rule"], rule.fields["type"], rule.fields["python"])
                    apiRulesObject.push(ruleObject)
                }
                setRulesObject(apiRulesObject)
                rulesToComponents()
            })
            .catch(error => {
                console.error('Error: ', error);
            });
    }

    async function addRule(textArea: string) {
        let textAreaObject = document.getElementById(textArea) as HTMLInputElement
        let valueOfTextArea = textAreaObject.value
        var ruleAdded = await addRuleToDatabase(valueOfTextArea)
        var badrule = document.getElementById("BadRules")
        //adding rule succeeded
        if (ruleAdded.FAIL == null) {
            badrule?.classList.remove("BadRulesShown")
            databaseToRules()
        }
        else {
            badrule?.classList.add("BadRulesShown")
        }
    }
     function apiToRules() {
         const data = new FormData();
         data.append("rule", "warehouse capacity < 50")
         fetch("http://localhost:8000/rules/add/", 
                     {method: 'POST',
                     mode: "cors",
                     body: data
                 } )
                 .then(response => {
                         return response.json();
                 })
                 .then(data => {
                     console.log('Success:', data);
                 })
                 .catch(error => {
                     console.error('Error: ', error);
                 });
     }

    function deleteFromRules(toDelete: string){
        var rules = rulesObject
        var index = 0
        for(let rule of rulesObject){
            if (rule.id === toDelete){
                rules.splice(index, 1)
            }
            index++
        }

        const data = new FormData();
        data.append("id", toDelete)
        fetch("http://localhost:8000/rules/remove",
            {
                method: 'POST',
                mode: "cors",
                body: data
            })
            .then(response => {
                return response.json();
            })
            .catch(error => {
                console.error('Error: ', error);
            });
        setRulesObject(rules)
        rulesToComponents()
    }

    function rulesToComponents() {
        var rulesComponents: JSX.Element[] = []
        for (let rule of rulesObject) {
            let ruleComponent: JSX.Element = <ListItem key={rule.id}>{rule.messy_rule}
                <Tooltip className="tooltip">Do you want to edit or delete this rule?
                <Button onClick={() => {
                    deleteFromRules(rule.id)
                    addRule("editTextArea")
                    }}
                >Edit</Button><Button className="deleteButton" onClick={() => {deleteFromRules(rule.id)}}>Delete</Button>
                <TextArea
                    labelText=""
                    id="editTextArea"
                    defaultValue={rule.messy_rule}
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