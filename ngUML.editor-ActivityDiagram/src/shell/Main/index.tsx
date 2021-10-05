import React from 'react'
import { EditorStateProvider } from '../../hooks/editorState'
import { EditorDataProvider } from '../../hooks/editorData'
import { TopMenu, NodeMenu, ContextMenu, Canvas } from '..'
import './_main.css'

export const Main: React.FC = () => {
    return (
        <EditorStateProvider>
            <EditorDataProvider>
                <TopMenu/>
                <NodeMenu/>
                <ContextMenu/>
                <Canvas/>
            </EditorDataProvider>
        </EditorStateProvider>
    )
}

export default Main