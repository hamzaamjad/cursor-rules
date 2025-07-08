# Extended content for prompt-eval

    },
    "task": {
      "objective": "[Specific, measurable goal for this prompt execution]",
      "success_criteria": [
        "[Criterion 1, e.g., Generated code passes linter]",
        "[Criterion 2, e.g., Output JSON validates against schema X]"
      ],
      "steps": [
        { "id": 1, "instruction": "[Step 1 instruction for the LLM]" },
        { "id": 2, "instruction": "[Step 2 instruction for the LLM]" }
        // Add more steps as needed
      ]
    },
    "examples": [
      {
        "id": "E1",
        "input": "[Example input data. Prefer structured object (JSON) over escaped strings if input is complex.]",
        "process": "[Optional: High-level description of process for this example]",
        "output": "[Example desired output corresponding to the input]"
      }
      // Add more few-shot examples if helpful (E2, E3...)
    ],
    "reasoning_guidance": {
      "approach": "[Suggested reasoning approach, e.g., Think step-by-step, Chain-of-thought]",
      "considerations": [
        "[Factor 1 to consider, e.g., Edge cases]",
        "[Factor 2 to consider, e.g., Performance implications]"
      ],
      "show_work": false, // Typically false for final output, true if debugging/transparency needed
      "evaluation_criteria": [
        "[Criterion for self-evaluation 1, e.g., Correctness]",
        "[Criterion for self-evaluation 2, e.g., Adherence to format]"
      ]
    },
    "output_specification": {
      "format": "[Expected output format, e.g., json, markdown, python_code]",
      "structure": "[Description or schema of the expected output structure]",
      "length": "[Constraint on length, e.g., <= 500 words, ~10 lines]",
      "validation_rules": [
        "[Rule 1 for validating the LLM's output, e.g., JSON must contain 'results' key]",
        "[Rule 2, e.g., Code must include type hints]"
      ],
      "excluded_elements": [
        "[Element 1 to exclude, e.g., Preamble/explanatory text]",
        "[Element 2 to exclude, e.g., Logging statements]"
      ]
    },
    "error_handling": {
      "ambiguity_resolution": {
        "protocol": "[How to handle ambiguity, e.g., Ask one clarifying question OR state assumptions.]",
        "max_iterations": 2
      },
      "missing_information": "[Action if info is missing, e.g., State what's missing; proceed best-effort or halt as instructed.]",
      "constraint_violations": {
        "action": "[Action if constraints violated, e.g., Halt and report violation.]"
      }
    }
}
```

*   **Changes**: Clarified the purpose – this file *is* the structural definition and the rule is to *use* this structure. Added explicit requirement to use this JSON structure. Added schema validation and completeness checks. Simplified the understanding of the rule's role. Reframed the JSON block as the structure definition / template example itself, using placeholders for content fields.
    *   *Added note to prefer structured JSON objects over escaped strings for complex nested data in `input_data.content` and `examples[*].input` based on retrospective feedback.* 
    *   *Added a validation check recommending programmatic JSON validation for complex generation.* 
    *   Added a requirement to ensure prompt content incorporates other relevant project rules.
    *   **Added requirements and validation checks for including diverse examples and comprehensive error handling guidance in research-oriented prompts.**
    *   **Added guidance to clarify essential vs. optional fields within the prompt template based on task complexity.**
*   **Source References**: `.cursor/rules/prompt-eval.mdc`