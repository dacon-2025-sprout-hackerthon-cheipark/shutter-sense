import Foundation
import UIKit
import Combine

@MainActor
class CameraViewModel: ObservableObject {
    @Published var selectedImage: UIImage?
    @Published var metadata: PhotoMetadata?
    @Published var predictions: PredictedSettings?
    @Published var suggestions: AIsuggestions?
    @Published var isLoading = false
    @Published var errorMessage: String?
    @Published var userPrompt: String = ""
    
    private let apiService = APIService.shared
    private let coreMLService = CoreMLService.shared
    
    /// Extract metadata from selected image
    func extractMetadata() async {
        guard let image = selectedImage else {
            errorMessage = "No image selected"
            return
        }
        
        isLoading = true
        errorMessage = nil
        
        do {
            let result = try await apiService.extractMetadata(from: image)
            metadata = result
        } catch {
            errorMessage = "Failed to extract metadata: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
    
    /// Predict camera settings
    func predictSettings() async {
        guard let image = selectedImage else {
            errorMessage = "No image selected"
            return
        }
        
        isLoading = true
        errorMessage = nil
        
        do {
            // Try CoreML first for local inference
            if let localPrediction = coreMLService.predictSettings(from: image) {
                predictions = localPrediction
            } else {
                // Fall back to API
                let result = try await apiService.predictSettings(from: image)
                predictions = result
            }
        } catch {
            errorMessage = "Failed to predict settings: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
    
    /// Get AI suggestions based on user prompt
    func getSuggestions() async {
        guard !userPrompt.isEmpty else {
            errorMessage = "Please enter a prompt"
            return
        }
        
        isLoading = true
        errorMessage = nil
        
        // Build current settings dictionary from metadata if available
        var currentSettings: [String: String]? = nil
        if let settings = metadata?.cameraSettings {
            currentSettings = [:]
            if let iso = settings.iso {
                currentSettings?["iso"] = "\(iso)"
            }
            if let aperture = settings.aperture {
                currentSettings?["aperture"] = aperture
            }
            if let shutter = settings.shutterSpeed {
                currentSettings?["shutter_speed"] = shutter
            }
        }
        
        do {
            let result = try await apiService.getSuggestions(
                prompt: userPrompt,
                currentSettings: currentSettings
            )
            suggestions = result
        } catch {
            errorMessage = "Failed to get suggestions: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
    
    /// Clear all data
    func clearData() {
        selectedImage = nil
        metadata = nil
        predictions = nil
        suggestions = nil
        errorMessage = nil
        userPrompt = ""
    }
}
