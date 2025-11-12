import SwiftUI
import PhotosUI

struct CameraView: View {
    @ObservedObject var viewModel: CameraViewModel
    @State private var showingImagePicker = false
    @State private var showingCamera = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                if let image = viewModel.selectedImage {
                    Image(uiImage: image)
                        .resizable()
                        .scaledToFit()
                        .frame(maxHeight: 300)
                        .cornerRadius(12)
                        .shadow(radius: 5)
                } else {
                    VStack(spacing: 15) {
                        Image(systemName: "camera.fill")
                            .font(.system(size: 80))
                            .foregroundColor(.gray)
                        
                        Text("No Image Selected")
                            .font(.headline)
                            .foregroundColor(.gray)
                    }
                    .frame(maxHeight: 300)
                }
                
                // Action buttons
                HStack(spacing: 15) {
                    Button(action: {
                        showingCamera = true
                    }) {
                        Label("Camera", systemImage: "camera")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    
                    Button(action: {
                        showingImagePicker = true
                    }) {
                        Label("Library", systemImage: "photo")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.green)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                }
                .padding(.horizontal)
                
                if viewModel.selectedImage != nil {
                    Button(action: {
                        viewModel.clearData()
                    }) {
                        Label("Clear", systemImage: "trash")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.red)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    .padding(.horizontal)
                }
                
                Spacer()
            }
            .padding()
            .navigationTitle("ShutterSense")
            .sheet(isPresented: $showingImagePicker) {
                ImagePicker(image: $viewModel.selectedImage)
            }
            .sheet(isPresented: $showingCamera) {
                CameraPicker(image: $viewModel.selectedImage)
            }
        }
    }
}
