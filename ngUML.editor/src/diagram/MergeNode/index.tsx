import { relative } from 'path'
import React from 'react'
import '../_decision_and_mergenode.css'
import {unEscapeCharacters,escapeCharacters,nl2br} from '../../commonFunctions'

interface IProperty {
    name: string;
    type: string;
}

interface INode {
    name: string;
    type: string;
    position: {
        x: number,
        y: number
    };
    data: Record<
        string,
        any
    >;
}

interface IMergeNode {
    node: INode;
    style?: React.CSSProperties;
    className?: string;
}

const MergeNode: React.FC<IMergeNode> = ({
    node,
    style: propStyle,
    className: propClassName,
}) => {
    const properties : IProperty[] = node['data']['properties'] ?? []

    return (
        <div className={'nguml-merge-node-wrapper'}>
        <div    
            style={{
                ...propStyle
            }}
            // className={propClassName}
            className={[propClassName, "nguml-merge-node"].join(" ")}
        >
        </div>
            {unEscapeCharacters(node.name)}
        </div>
    )
}

export default MergeNode