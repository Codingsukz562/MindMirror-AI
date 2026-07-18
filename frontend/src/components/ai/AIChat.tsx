import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Sparkles, X, Bot, User } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { API_BASE_URL } from '@/services/api'

interface ChatMessage {
  id: string
  role: 'user' | 'assistant' | 'error'
  content: string
  timestamp: Date
}

interface ChatSuggestion {
  text: string
}

interface AIChatProps {
  habitId: string
  onClose?: () => void
}

export default function AIChat({ habitId, onClose }: AIChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content:
        "Hi! I'm your MindMirror AI coach. I'm here to support you on your journey. What's on your mind today?",
      timestamp: new Date(),
    },
  ])

  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [suggestions, setSuggestions] = useState<ChatSuggestion[]>([])

  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    fetchSuggestions()
  }, [habitId])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: 'smooth',
    })
  }, [messages])


  const fetchSuggestions = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/habits/${habitId}/chat/suggestions`
      )

      if (response.ok) {
        const data = await response.json()
        setSuggestions(data.suggestions || [])
      }

    } catch (error) {
      console.error('Failed to fetch suggestions:', error)
    }
  }


  const sendMessage = async () => {

    if (!input.trim() || isLoading) {
      return
    }


    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    }


    setMessages(prev => [
      ...prev,
      userMessage
    ])

    setInput('')
    setIsLoading(true)


    try {

      const response = await fetch(
        `${API_BASE_URL}/api/habits/${habitId}/chat`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },

          /*
            FIX:
            Backend expects:

            {
              "message": "text"
            }

            Earlier we were sending:

            {
              "message": {
                  "message":"text"
              }
            }

          */

          body: JSON.stringify({
            message: userMessage.content,
            context: {
              reflections_count: messages.length,
            },
          }),
        }
      )


      if (!response.ok) {
        throw new Error(
          `Chat failed with status ${response.status}`
        )
      }


      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '',
        timestamp: new Date(),
      }


      setMessages(prev => [
        ...prev,
        assistantMessage,
      ])


      const reader = response.body?.getReader()


      if (!reader) {

        throw new Error(
          'Streaming response unavailable'
        )
      }


      const decoder = new TextDecoder()


      while (true) {

        const {
          done,
          value,
        } = await reader.read()


        if (done) {
          break
        }


        const chunk = decoder.decode(
          value,
          {
            stream: true,
          }
        )


        const lines = chunk.split('\n')


        for (const line of lines) {


          if (!line.startsWith('data: ')) {
            continue
          }


          try {

            const data = JSON.parse(
              line.substring(6)
            )


            if (data.type === 'message') {

              setMessages(prev =>
                prev.map(msg =>
                  msg.id === assistantMessage.id
                    ? {
                        ...msg,
                        content: data.content,
                      }
                    : msg
                )
              )

            }


            if (data.type === 'error') {

              setMessages(prev =>
                prev.map(msg =>
                  msg.id === assistantMessage.id
                    ? {
                        ...msg,
                        role: 'error',
                        content: data.content,
                      }
                    : msg
                )
              )

            }


          } catch (error) {

            console.warn(
              'Invalid stream response:',
              line
            )

          }

        }

      }


    } catch (error) {


      console.error(
        'Chat error:',
        error
      )


      const errorMessage: ChatMessage = {

        id: (Date.now() + 1).toString(),

        role: 'error',

        content:
          "I apologize, but I'm having trouble connecting right now. Please try again in a moment.",

        timestamp: new Date(),

      }


      setMessages(prev => [
        ...prev,
        errorMessage,
      ])


    } finally {

      setIsLoading(false)

    }

  }



  const handleSuggestionClick = (
    suggestion: string
  ) => {

    setInput(suggestion)

  }



  const handleKeyDown = (
    e: React.KeyboardEvent
  ) => {

    if (
      e.key === 'Enter'
      &&
      !e.shiftKey
    ) {

      e.preventDefault()

      sendMessage()

    }

  }



  return (

    <Card className="glass-card flex flex-col h-[600px] max-h-[80vh]">

      <div className="flex items-center justify-between p-4 border-b">

        <div className="flex items-center gap-3">

          <div className="p-2 rounded-full bg-primary/20">

            <Bot className="h-5 w-5 text-primary" />

          </div>


          <div>

            <h3 className="font-semibold">
              MindMirror AI Coach
            </h3>

            <p className="text-xs text-muted-foreground">
              Always here to support you
            </p>

          </div>

        </div>


        {
          onClose &&
          (
            <Button
              variant="ghost"
              size="icon"
              onClick={onClose}
            >

              <X className="h-4 w-4"/>

            </Button>
          )
        }

      </div>



      <div className="flex-1 overflow-y-auto p-4 space-y-4">

        <AnimatePresence>

          {
            messages.map(message => (

              <motion.div

                key={message.id}

                initial={{
                  opacity:0,
                  y:10
                }}

                animate={{
                  opacity:1,
                  y:0
                }}

                className={`flex gap-3 ${
                  message.role === 'user'
                  ? 'flex-row-reverse'
                  : 'flex-row'
                }`}

              >

                <div className="p-2 rounded-full bg-primary/20 h-8 w-8 flex items-center justify-center">

                  {
                    message.role === 'user'
                    ?
                    <User className="h-4 w-4"/>
                    :
                    <Bot className="h-4 w-4"/>
                  }

                </div>


                <div className="max-w-[70%] p-3 rounded-lg bg-muted">

                  <p className="text-sm whitespace-pre-wrap">

                    {message.content}

                  </p>

                </div>


              </motion.div>

            ))
          }

        </AnimatePresence>



        {
          isLoading &&
          (

            <div className="flex gap-3">

              <div className="p-2 rounded-full bg-primary/20">

                <Bot className="h-4 w-4"/>

              </div>


              <div className="bg-muted p-3 rounded-lg">

                <Sparkles className="h-4 w-4 animate-pulse"/>

              </div>


            </div>

          )
        }


        <div ref={messagesEndRef}/>

      </div>




      {
        suggestions.length > 0 &&
        !isLoading &&
        (

          <div className="px-4 py-2 border-t">

            <p className="text-xs text-muted-foreground mb-2">
              Try asking:
            </p>


            <div className="flex flex-wrap gap-2">

              {
                suggestions.map(
                  (suggestion,index)=>(

                    <Button

                      key={index}

                      variant="outline"

                      size="sm"

                      onClick={() =>
                        handleSuggestionClick(
                          suggestion.text
                        )
                      }

                    >

                      {suggestion.text}

                    </Button>

                  )
                )
              }

            </div>


          </div>

        )
      }





      <div className="p-4 border-t">

        <div className="flex gap-2">

          <Textarea

            value={input}

            onChange={
              e => setInput(
                e.target.value
              )
            }

            onKeyDown={handleKeyDown}

            placeholder="Share what's on your mind..."

            disabled={isLoading}

            rows={2}

          />


          <Button

            onClick={sendMessage}

            disabled={
              !input.trim()
              ||
              isLoading
            }

            size="icon"

          >

            {
              isLoading
              ?
              <Sparkles className="h-4 w-4 animate-pulse"/>
              :
              <Send className="h-4 w-4"/>
            }


          </Button>


        </div>


      </div>


    </Card>

  )
}