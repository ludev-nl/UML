import React, { useState } from 'react'
import './_rulemenu.css'
import {
    TextArea,
    Button,
    OrderedList,
    ListItem,
    Tooltip
} from 'carbon-components-react'
import { useEffect } from 'react'

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
    useEffect(() => databaseToRules())

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
        fetch("http://localhost:8000/rules/",
            {
                method: 'GET',
                mode: "cors",
            })
            .then(response => {
                return response.json();
            })
            .then(response => {
                var apiRulesObject: RuleObject[] = []
                for (var rule of response) {
                    var ruleObject: RuleObject = new RuleObject(rule.pk, rule.fields["original_input"], rule.fields["processed_text"], rule.fields["type"], "")
                    apiRulesObject.push(ruleObject)
                }
                rulesToComponents(apiRulesObject)
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
            badrule?.classList.add("GoodRulesShown")
            badrule!.innerHTML = "Rule successfully added"
            databaseToRules()
        }
        else {
            badrule?.classList.add("BadRulesShown")
            badrule?.classList.remove("GoodRulesShown")
            badrule!.innerHTML = "Bad rule entered"
        }
    }

    function deleteFromRules(toDelete: string){

        const data = new FormData();
        data.append("pk", toDelete)
        fetch("http://localhost:8000/rules/remove/",
            {
                method: 'POST',
                mode: "cors",
                body: data
            })
            .then(response => {
                databaseToRules()
                return response.json();
            })
            .catch(error => {
                console.error('Error: ', error);
            });
    }

    function rulesToComponents(rulesObject: RuleObject[]) {
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
                
            </span>
            <hr>
            </hr>
            <OrderedList
                id="ruleList"
            >
                {rulesState}
            </OrderedList>
        </div>
    )
}

export default RuleMenu