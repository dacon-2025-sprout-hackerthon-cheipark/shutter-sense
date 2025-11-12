import Foundation

/// Camera settings model
struct CameraSettings: Codable {
    var iso: Int?
    var aperture: String?
    var shutterSpeed: String?
    var focalLength: String?
    var cameraMake: String?
    var cameraModel: String?
    var lensModel: String?
    var whiteBalance: Int?
}

/// Metadata response from API
struct MetadataResponse: Codable {
    let success: Bool
    let metadata: PhotoMetadata
}

/// Photo metadata structure
struct PhotoMetadata: Codable {
    let format: String?
    let mode: String?
    let size: ImageSize?
    let cameraSettings: CameraSettings?
    
    enum CodingKeys: String, CodingKey {
        case format, mode, size
        case cameraSettings = "camera_settings"
    }
}

/// Image size
struct ImageSize: Codable {
    let width: Int
    let height: Int
}

/// Prediction response from API
struct PredictionResponse: Codable {
    let success: Bool
    let predictions: PredictedSettings
}

/// Predicted camera settings
struct PredictedSettings: Codable {
    let iso: Int?
    let aperture: String?
    let shutterSpeed: String?
    let avgBrightness: Double?
    let confidence: Double?
    let note: String?
    
    enum CodingKeys: String, CodingKey {
        case iso, aperture, confidence, note
        case shutterSpeed = "shutter_speed"
        case avgBrightness = "avg_brightness"
    }
}

/// Suggestion request for LLM
struct SuggestionRequest: Codable {
    let prompt: String
    let currentSettings: [String: String]?
    
    enum CodingKeys: String, CodingKey {
        case prompt
        case currentSettings = "current_settings"
    }
}

/// Suggestion response from API
struct SuggestionResponse: Codable {
    let success: Bool
    let suggestions: AIsuggestions
}

/// AI-generated suggestions
struct AIsuggestions: Codable {
    let iso: Int?
    let aperture: String?
    let shutterSpeed: String?
    let explanation: String?
    let source: String?
    
    enum CodingKeys: String, CodingKey {
        case iso, aperture, explanation, source
        case shutterSpeed = "shutter_speed"
    }
}
