#! /usr/bin/env bash


curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2:1b-instruct-q4_0",
  "messages": [
    {
      "role": "system",
      "content": "Datetime: 21-06-2025. You are a medical assistant, that manage personal info like medical history, medical tests and amy other personal things. Your patient is a matrix user with id hena@dezart.by. He was joined matrix server in 15 of june 2025. If you do not have some personal info, give user instruction that he should upload the message with this info."
    },
    {
      "role": "system",
      "content": "Metadata: User call hena@dezart.by. Patient tests     tests: {blood test: {blood_test_results: {date: 2025-06-15,CBC: {WBC: {value: 6.2,unit: x10^3/µL,reference_range: 4.0-11.0},RBC: {value: 4.8,unit: x10^6/µL,reference_range: 4.5-6.0},Hemoglobin: {value: 14.7,unit: g/dL,reference_range: 13.5-17.5 },Hematocrit: {value: 44,unit: %,reference_range: 38.8-50.0},Platelets: {value: 210,unit: x10^3/µL, reference_range: 150-400}},CMP: {Glucose: {value: 92,unit: mg/dL,reference_range: 70-99},Calcium: {value: 9.4, unit: mg/dL,reference_range: 8.5-10.2},Sodium: {value: 138,unit: mmol/L,reference_range: 135-145},Potassium: {value: 4.1,unit: mmol/L,reference_range: 3.5-5.1},Chloride: {value: 101,unit: mmol/L,reference_range: 98-107},BUN: {value: 14,unit: mg/dL,reference_range: 7-20},Creatinine: {value: 1,unit: mg/dL,reference_range: 0.6-1.3},ALT: {value: 25,unit: U/L,reference_range: 7-56 },AST: {value: 22,unit: U/L,reference_range: 10-40}},Lipid_Profile: {Total_Cholesterol: {value: 185,unit: mg/dL,reference_range: <200},HDL: {value: 55,unit: mg/dL,reference_range: 40-60},LDL: {value: 110,unit: mg/dL,reference_range: <130},Triglycerides: {value: 130,unit: mg/dL,reference_range: <150}}}}},"
    },
    {
      "role": "user",
      "content": "Do you have my tests?"
    }
  ],
  "stream": false,
  "options": {
    "temperature": 0.1
  }
}'