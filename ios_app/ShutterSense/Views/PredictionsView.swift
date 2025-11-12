import SwiftUI

struct PredictionsView: View {
    @ObservedObject var viewModel: CameraViewModel
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    if viewModel.selectedImage == nil {
                        VStack(spacing: 15) {
                            Image(systemName: "cpu")
                                .font(.system(size: 60))
                                .foregroundColor(.gray)
                            
                            Text("Select an image to predict settings")
                                .font(.headline)
                                .foregroundColor(.gray)
                        }
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                        .padding(.top, 100)
                    } else {
                        // Predict button
                        Button(action: {
                            Task {
                                await viewModel.predictSettings()
                            }
                        }) {
                            HStack {
                                if viewModel.isLoading {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle())
                                } else {
                                    Image(systemName: "cpu")
                                }
                                Text("Predict Settings")
                            }
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.purple)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                        }
                        .disabled(viewModel.isLoading)
                        .padding()
                        
                        // Display predictions
                        if let predictions = viewModel.predictions {
                            VStack(alignment: .leading, spacing: 15) {
                                SectionHeader(title: "Predicted Settings")
                                
                                if let iso = predictions.iso {
                                    PredictionCard(
                                        icon: "sun.max",
                                        label: "ISO",
                                        value: "\(iso)",
                                        color: .orange
                                    )
                                }
                                
                                if let aperture = predictions.aperture {
                                    PredictionCard(
                                        icon: "circle.hexagonpath",
                                        label: "Aperture",
                                        value: aperture,
                                        color: .blue
                                    )
                                }
                                
                                if let shutter = predictions.shutterSpeed {
                                    PredictionCard(
                                        icon: "timer",
                                        label: "Shutter Speed",
                                        value: shutter,
                                        color: .green
                                    )
                                }
                                
                                if let brightness = predictions.avgBrightness {
                                    InfoRow(
                                        label: "Avg Brightness",
                                        value: String(format: "%.1f", brightness)
                                    )
                                }
                                
                                if let confidence = predictions.confidence {
                                    HStack {
                                        Text("Confidence")
                                            .foregroundColor(.secondary)
                                        Spacer()
                                        ProgressView(value: confidence)
                                            .frame(width: 100)
                                        Text(String(format: "%.0f%%", confidence * 100))
                                            .fontWeight(.medium)
                                    }
                                    .padding(.vertical, 4)
                                }
                                
                                if let note = predictions.note {
                                    Text(note)
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                        .padding()
                                        .background(Color.gray.opacity(0.1))
                                        .cornerRadius(8)
                                }
                            }
                            .padding()
                        }
                        
                        if let error = viewModel.errorMessage {
                            ErrorView(message: error)
                                .padding()
                        }
                    }
                }
            }
            .navigationTitle("Predictions")
        }
    }
}

struct PredictionCard: View {
    let icon: String
    let label: String
    let value: String
    let color: Color
    
    var body: some View {
        HStack(spacing: 15) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(color)
                .frame(width: 40)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(label)
                    .font(.caption)
                    .foregroundColor(.secondary)
                Text(value)
                    .font(.title3)
                    .fontWeight(.semibold)
            }
            
            Spacer()
        }
        .padding()
        .background(color.opacity(0.1))
        .cornerRadius(12)
    }
}
