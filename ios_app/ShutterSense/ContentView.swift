import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = CameraViewModel()
    @State private var showingImagePicker = false
    @State private var showingCamera = false
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            // Camera/Photo Tab
            CameraView(viewModel: viewModel)
                .tabItem {
                    Label("Camera", systemImage: "camera")
                }
                .tag(0)
            
            // Metadata Tab
            MetadataView(viewModel: viewModel)
                .tabItem {
                    Label("Metadata", systemImage: "info.circle")
                }
                .tag(1)
            
            // Predictions Tab
            PredictionsView(viewModel: viewModel)
                .tabItem {
                    Label("Predict", systemImage: "cpu")
                }
                .tag(2)
            
            // AI Suggestions Tab
            SuggestionsView(viewModel: viewModel)
                .tabItem {
                    Label("AI Suggest", systemImage: "sparkles")
                }
                .tag(3)
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
