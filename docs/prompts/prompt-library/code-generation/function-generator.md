# Prompt: Function Generator

Generate well-structured functions from natural language descriptions.

---

## Purpose

Use this prompt to generate clean, documented functions from descriptions. Ideal for utility functions, algorithms, and business logic.

---

## Prompt

```
Generate a {language} function with the following specifications:

## Function Purpose
{description}

## Requirements
- Input: {input_description}
- Output: {output_description}
- {additional_requirements}

## Constraints
- {constraints}
- Include TypeScript types if applicable
- Follow {style_guide} style guidelines
- Handle edge cases appropriately

## Expected Behavior
{behavior_description}

## Example
Input: {example_input}
Output: {example_output}

Please provide:
1. The function implementation with type definitions
2. JSDoc/TSDoc documentation
3. Brief explanation of the approach
4. Example usage
```

---

## Parameters

| Parameter | Description | Required | Example |
|-----------|-------------|----------|---------|
| {language} | Target programming language | Yes | TypeScript, Python |
| {description} | What the function should do | Yes | "Calculate the total price with tax and discount" |
| {input_description} | Input parameters and types | Yes | "price: number, taxRate: number, discount?: number" |
| {output_description} | Return type and description | Yes | "number - the final price" |
| {additional_requirements} | Any specific requirements | No | "Round to 2 decimal places" |
| {constraints} | Limitations to consider | No | "Handle negative values by returning 0" |
| {style_guide} | Coding style to follow | No | "Airbnb", "Google" |
| {behavior_description} | Detailed behavior | No | Edge cases, error handling |
| {example_input} | Sample input | No | "100, 0.1, 5" |
| {example_output} | Expected output | No | "104.5" |

---

## Example Usage

### Filled Prompt

```
Generate a TypeScript function with the following specifications:

## Function Purpose
Calculate the total price with tax and optional discount applied.

## Requirements
- Input: price: number, taxRate: number, discount?: number
- Output: number - the final price rounded to 2 decimal places
- Apply discount before tax if provided

## Constraints
- Handle negative values by throwing an error
- Include TypeScript types
- Follow Airbnb style guidelines
- Handle edge cases appropriately

## Expected Behavior
- If discount is provided, subtract it from price first
- Apply tax rate to the discounted price
- Round result to 2 decimal places

## Example
Input: 100, 0.1, 5
Output: 104.5

Please provide:
1. The function implementation with type definitions
2. JSDoc/TSDoc documentation
3. Brief explanation of the approach
4. Example usage
```

---

## Tips

1. **Be specific about types** - Include exact type definitions needed
2. **Describe edge cases** - How should the function handle unusual inputs?
3. **Include constraints** - Any limitations or requirements
4. **Provide examples** - Concrete input/output pairs help accuracy
5. **Specify error handling** - Should it throw, return null, etc.?

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-13 | Initial version |
