import React from 'react'

interface IEnumNode {
    node: any;
}

const EnumNode: React.FC<IEnumNode> = ({node}) => {
    return (
        <div>
            {node.name}
        </div>
    )
}

export default EnumNode
