#!/usr/bin/env python3
"""
Create better training data for CodeT5 model.
This script generates high-quality Postman JavaScript test examples.
"""

import json
import random
from typing import List, Dict, Any

def create_better_training_data():
    """Create high-quality training data with proper Postman JavaScript tests."""
    
    training_samples = []
    
    # Sample 1: GET endpoint with 200 response
    sample1 = {
        "input": "Generate Postman JavaScript tests for: GET /api/users - Validate successful user list retrieval",
        "output": """pm.test("Response status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has JSON content type", function () {
    pm.response.to.have.header("Content-Type");
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});

pm.test("Response structure is valid", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.be.an('object');
    pm.expect(responseData).to.have.property('users');
    pm.expect(responseData.users).to.be.an('array');
});

pm.test("Users have required fields", function () {
    const responseData = pm.response.json();
    if (responseData.users.length > 0) {
        const firstUser = responseData.users[0];
        pm.expect(firstUser).to.have.property('id');
        pm.expect(firstUser).to.have.property('name');
        pm.expect(firstUser).to.have.property('email');
    }
});"""
    }
    training_samples.append(sample1)
    
    # Sample 2: POST endpoint with 201 response
    sample2 = {
        "input": "Generate Postman JavaScript tests for: POST /api/users - Validate successful user creation",
        "output": """pm.test("Response status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Response has JSON content type", function () {
    pm.response.to.have.header("Content-Type");
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});

pm.test("Response contains created user data", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.be.an('object');
    pm.expect(responseData).to.have.property('id');
    pm.expect(responseData).to.have.property('name');
    pm.expect(responseData).to.have.property('email');
    pm.expect(responseData.id).to.be.a('number');
});

pm.test("Created user matches request data", function () {
    const responseData = pm.response.json();
    const requestData = JSON.parse(pm.request.body.raw);
    pm.expect(responseData.name).to.equal(requestData.name);
    pm.expect(responseData.email).to.equal(requestData.email);
});"""
    }
    training_samples.append(sample2)
    
    # Sample 3: GET endpoint with 404 response
    sample3 = {
        "input": "Generate Postman JavaScript tests for: GET /api/users/999999 - Validate 404 error response",
        "output": """pm.test("Response status code is 404", function () {
    pm.response.to.have.status(404);
});

pm.test("Error response has correct structure", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.be.an('object');
    pm.expect(responseData).to.have.property('error');
    pm.expect(responseData).to.have.property('message');
    pm.expect(responseData).to.have.property('statusCode');
    pm.expect(responseData.statusCode).to.equal(404);
});

pm.test("Error message is descriptive", function () {
    const responseData = pm.response.json();
    pm.expect(responseData.message).to.include('not found');
    pm.expect(responseData.error).to.equal('Not Found');
});"""
    }
    training_samples.append(sample3)
    
    # Sample 4: PUT endpoint with 200 response
    sample4 = {
        "input": "Generate Postman JavaScript tests for: PUT /api/users/123 - Validate successful user update",
        "output": """pm.test("Response status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains updated user data", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.be.an('object');
    pm.expect(responseData).to.have.property('id');
    pm.expect(responseData).to.have.property('name');
    pm.expect(responseData).to.have.property('email');
    pm.expect(responseData.id).to.equal(123);
});

pm.test("Updated user matches request data", function () {
    const responseData = pm.response.json();
    const requestData = JSON.parse(pm.request.body.raw);
    pm.expect(responseData.name).to.equal(requestData.name);
    pm.expect(responseData.email).to.equal(requestData.email);
});

pm.test("Response includes updated timestamp", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.have.property('updatedAt');
    pm.expect(responseData.updatedAt).to.be.a('string');
});"""
    }
    training_samples.append(sample4)
    
    # Sample 5: DELETE endpoint with 204 response
    sample5 = {
        "input": "Generate Postman JavaScript tests for: DELETE /api/users/123 - Validate successful user deletion",
        "output": """pm.test("Response status code is 204", function () {
    pm.response.to.have.status(204);
});

pm.test("Response body is empty", function () {
    pm.expect(pm.response.text()).to.be.empty;
});

pm.test("Response has no content type header", function () {
    pm.expect(pm.response.headers.get("Content-Type")).to.be.undefined;
});"""
    }
    training_samples.append(sample5)
    
    # Sample 6: POST endpoint with 400 validation error
    sample6 = {
        "input": "Generate Postman JavaScript tests for: POST /api/users - Validate 400 validation error",
        "output": """pm.test("Response status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Error response has validation structure", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.be.an('object');
    pm.expect(responseData).to.have.property('error');
    pm.expect(responseData).to.have.property('message');
    pm.expect(responseData).to.have.property('statusCode');
    pm.expect(responseData.statusCode).to.equal(400);
});

pm.test("Error message indicates validation failure", function () {
    const responseData = pm.response.json();
    pm.expect(responseData.message).to.include('validation');
    pm.expect(responseData.error).to.equal('Bad Request');
});"""
    }
    training_samples.append(sample6)
    
    # Sample 7: GET endpoint with authentication
    sample7 = {
        "input": "Generate Postman JavaScript tests for: GET /api/profile - Validate authenticated user profile",
        "output": """pm.test("Response status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains user profile data", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.be.an('object');
    pm.expect(responseData).to.have.property('id');
    pm.expect(responseData).to.have.property('username');
    pm.expect(responseData).to.have.property('email');
    pm.expect(responseData).to.have.property('profile');
});

pm.test("Profile data is complete", function () {
    const responseData = pm.response.json();
    pm.expect(responseData.profile).to.have.property('firstName');
    pm.expect(responseData.profile).to.have.property('lastName');
    pm.expect(responseData.profile).to.have.property('avatar');
});

pm.test("User ID matches authenticated user", function () {
    const responseData = pm.response.json();
    const authToken = pm.request.headers.get('Authorization');
    // Note: In real scenario, you might decode JWT token to verify user ID
    pm.expect(responseData.id).to.be.a('number');
});"""
    }
    training_samples.append(sample7)
    
    # Sample 8: GET endpoint with pagination
    sample8 = {
        "input": "Generate Postman JavaScript tests for: GET /api/orders - Validate paginated order list",
        "output": """pm.test("Response status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has pagination structure", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.be.an('object');
    pm.expect(responseData).to.have.property('data');
    pm.expect(responseData).to.have.property('pagination');
    pm.expect(responseData.data).to.be.an('array');
});

pm.test("Pagination metadata is correct", function () {
    const responseData = pm.response.json();
    pm.expect(responseData.pagination).to.have.property('page');
    pm.expect(responseData.pagination).to.have.property('limit');
    pm.expect(responseData.pagination).to.have.property('total');
    pm.expect(responseData.pagination).to.have.property('pages');
    pm.expect(responseData.pagination.page).to.be.a('number');
    pm.expect(responseData.pagination.limit).to.be.a('number');
});

pm.test("Orders have required fields", function () {
    const responseData = pm.response.json();
    if (responseData.data.length > 0) {
        const firstOrder = responseData.data[0];
        pm.expect(firstOrder).to.have.property('id');
        pm.expect(firstOrder).to.have.property('customerId');
        pm.expect(firstOrder).to.have.property('status');
        pm.expect(firstOrder).to.have.property('total');
    }
});"""
    }
    training_samples.append(sample8)
    
    # Sample 9: POST endpoint with 401 unauthorized
    sample9 = {
        "input": "Generate Postman JavaScript tests for: POST /api/orders - Validate 401 unauthorized error",
        "output": """pm.test("Response status code is 401", function () {
    pm.response.to.have.status(401);
});

pm.test("Error response has authentication structure", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.be.an('object');
    pm.expect(responseData).to.have.property('error');
    pm.expect(responseData).to.have.property('message');
    pm.expect(responseData).to.have.property('statusCode');
    pm.expect(responseData.statusCode).to.equal(401);
});

pm.test("Error message indicates authentication failure", function () {
    const responseData = pm.response.json();
    pm.expect(responseData.message).to.include('unauthorized');
    pm.expect(responseData.error).to.equal('Unauthorized');
});"""
    }
    training_samples.append(sample9)
    
    # Sample 10: GET endpoint with 500 server error
    sample10 = {
        "input": "Generate Postman JavaScript tests for: GET /api/system/status - Validate 500 server error",
        "output": """pm.test("Response status code is 500", function () {
    pm.response.to.have.status(500);
});

pm.test("Error response has server error structure", function () {
    const responseData = pm.response.json();
    pm.expect(responseData).to.be.an('object');
    pm.expect(responseData).to.have.property('error');
    pm.expect(responseData).to.have.property('message');
    pm.expect(responseData).to.have.property('statusCode');
    pm.expect(responseData.statusCode).to.equal(500);
});

pm.test("Error message indicates server error", function () {
    const responseData = pm.response.json();
    pm.expect(responseData.message).to.include('server');
    pm.expect(responseData.error).to.equal('Internal Server Error');
});"""
    }
    training_samples.append(sample10)
    
    # Write to file
    with open("better_training_data.jsonl", "w", encoding="utf-8") as f:
        for sample in training_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
    
    print(f"✅ Created better training data with {len(training_samples)} high-quality samples")
    print("📁 File: better_training_data.jsonl")
    
    return training_samples

if __name__ == "__main__":
    create_better_training_data() 