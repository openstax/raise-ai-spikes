import { Formik, Form, Field, FormikHelpers, ErrorMessage, FieldInputProps } from 'formik'
import styled from 'styled-components'
import { useState } from 'react'

const StyledForm = styled(Form)`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
`

const InputContainer = styled.div`
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
`

const Button = styled.button`
  align-items: center;
  margin: 10px;
  min-width: 95px;
  height: 35px;
  color: black;
  background-color: #87CEEB;
    &:disabled {
      background-color: grey;
      color: white;

    }
`

const InputLabel = styled.label`
  text-align: center;
  margin-bottom: 5px;
`

const InputField = styled.input`
  max-width:800px;
  max-height:800px;
  min-width: 700px;
  max-height: 300px;
  min-height: 200px;
  padding: 8px;
  border: 2px solid black;

`

const StyledErrorMessage = styled(ErrorMessage)`
  color: red;
  text-align: center;
  `


interface TextInputFormProps {
  onSubmit: (input: string) => Promise<void>
}

export function TextInputForm({onSubmit}: TextInputFormProps)  :JSX.Element {
  const initialValues = {
    userInput: '',
  }
  const [isSubmitting, setIsSubmitting] = useState(false)
  const validate = (values: { userInput: string }) => {
    const errors: { userInput?: string } = {}
    if (!values.userInput.trim()) {
      errors.userInput = 'Input cannot be empty'
    }
    if (values.userInput.length > 5000){
      errors.userInput = 'Input exceeds the character limit of 5000 characters'
    }
    return errors
  }

  const handleSubmit = async (values: { userInput: string }, { resetForm }: FormikHelpers<{ userInput: string }>) => {
    setIsSubmitting(true)
    try {
      await onSubmit(values.userInput)
      resetForm()
    } finally {
      setIsSubmitting(false)
    }
  }
  const FormField = ({
    field,
    ...props
  }: {
    field: FieldInputProps<string>
  }) => {
    return <InputField as="textarea" {...field} {...props} />
  }

  return (
    <Formik initialValues={initialValues} onSubmit={handleSubmit} validate={validate}>
      {({ handleSubmit }) => (
        <StyledForm onSubmit={handleSubmit}>
          <InputContainer>
            <InputLabel>Text input </InputLabel>
            <Field disabled={isSubmitting} name="userInput" component={FormField} />
            <StyledErrorMessage name="userInput" component="div" className="error" />
          </InputContainer>

          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Finding Resourses...' : 'Search'}
          </Button>
        </StyledForm>
      )}
    </Formik>
  )
}
