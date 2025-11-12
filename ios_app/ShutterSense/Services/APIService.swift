import Foundation
import UIKit
import Combine

class APIService {
    static let shared = APIService()
    
    // Configure your backend URL
    private let baseURL = "http://localhost:8000"
    
    private init() {}
    
    /// Extract metadata from image
    func extractMetadata(from image: UIImage) async throws -> PhotoMetadata {
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            throw APIError.invalidImage
        }
        
        let url = URL(string: "\(baseURL)/metadata")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        // Create multipart form data
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"photo.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw APIError.invalidResponse
        }
        
        let decoder = JSONDecoder()
        let result = try decoder.decode(MetadataResponse.self, from: data)
        
        return result.metadata
    }
    
    /// Predict camera settings
    func predictSettings(from image: UIImage) async throws -> PredictedSettings {
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            throw APIError.invalidImage
        }
        
        let url = URL(string: "\(baseURL)/predict")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        // Create multipart form data
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"photo.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw APIError.invalidResponse
        }
        
        let decoder = JSONDecoder()
        let result = try decoder.decode(PredictionResponse.self, from: data)
        
        return result.predictions
    }
    
    /// Get AI suggestions based on prompt
    func getSuggestions(prompt: String, currentSettings: [String: String]? = nil) async throws -> AIsuggestions {
        let url = URL(string: "\(baseURL)/suggest")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let suggestionRequest = SuggestionRequest(prompt: prompt, currentSettings: currentSettings)
        let encoder = JSONEncoder()
        request.httpBody = try encoder.encode(suggestionRequest)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw APIError.invalidResponse
        }
        
        let decoder = JSONDecoder()
        let result = try decoder.decode(SuggestionResponse.self, from: data)
        
        return result.suggestions
    }
}

enum APIError: Error {
    case invalidImage
    case invalidResponse
    case networkError
}
