import SwiftUI

struct MetadataView: View {
    @ObservedObject var viewModel: CameraViewModel
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    if viewModel.selectedImage == nil {
                        VStack(spacing: 15) {
                            Image(systemName: "info.circle")
                                .font(.system(size: 60))
                                .foregroundColor(.gray)
                            
                            Text("Select an image to view metadata")
                                .font(.headline)
                                .foregroundColor(.gray)
                        }
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                        .padding(.top, 100)
                    } else {
                        // Extract button
                        Button(action: {
                            Task {
                                await viewModel.extractMetadata()
                            }
                        }) {
                            HStack {
                                if viewModel.isLoading {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle())
                                } else {
                                    Image(systemName: "arrow.down.doc")
                                }
                                Text("Extract Metadata")
                            }
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                        }
                        .disabled(viewModel.isLoading)
                        .padding()
                        
                        // Display metadata
                        if let metadata = viewModel.metadata {
                            VStack(alignment: .leading, spacing: 15) {
                                SectionHeader(title: "Image Info")
                                
                                if let format = metadata.format {
                                    InfoRow(label: "Format", value: format)
                                }
                                
                                if let size = metadata.size {
                                    InfoRow(label: "Size", value: "\(size.width) × \(size.height)")
                                }
                                
                                if let settings = metadata.cameraSettings {
                                    Divider()
                                    SectionHeader(title: "Camera Settings")
                                    
                                    if let iso = settings.iso {
                                        InfoRow(label: "ISO", value: "\(iso)")
                                    }
                                    
                                    if let aperture = settings.aperture {
                                        InfoRow(label: "Aperture", value: aperture)
                                    }
                                    
                                    if let shutter = settings.shutterSpeed {
                                        InfoRow(label: "Shutter Speed", value: shutter)
                                    }
                                    
                                    if let focal = settings.focalLength {
                                        InfoRow(label: "Focal Length", value: focal)
                                    }
                                    
                                    if let make = settings.cameraMake {
                                        InfoRow(label: "Camera Make", value: make)
                                    }
                                    
                                    if let model = settings.cameraModel {
                                        InfoRow(label: "Camera Model", value: model)
                                    }
                                    
                                    if let lens = settings.lensModel {
                                        InfoRow(label: "Lens", value: lens)
                                    }
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
            .navigationTitle("Metadata")
        }
    }
}

struct SectionHeader: View {
    let title: String
    
    var body: some View {
        Text(title)
            .font(.headline)
            .foregroundColor(.primary)
            .padding(.vertical, 5)
    }
}

struct InfoRow: View {
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(label)
                .foregroundColor(.secondary)
            Spacer()
            Text(value)
                .fontWeight(.medium)
        }
        .padding(.vertical, 4)
    }
}

struct ErrorView: View {
    let message: String
    
    var body: some View {
        HStack {
            Image(systemName: "exclamationmark.triangle")
            Text(message)
                .font(.caption)
        }
        .foregroundColor(.red)
        .padding()
        .background(Color.red.opacity(0.1))
        .cornerRadius(8)
    }
}
