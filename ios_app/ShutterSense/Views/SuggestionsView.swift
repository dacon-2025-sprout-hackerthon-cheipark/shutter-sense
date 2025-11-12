import SwiftUI

struct SuggestionsView: View {
    @ObservedObject var viewModel: CameraViewModel
    @FocusState private var isTextFieldFocused: Bool
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    // Prompt input
                    VStack(alignment: .leading, spacing: 10) {
                        Text("Describe your photography scenario")
                            .font(.headline)
                            .padding(.horizontal)
                        
                        TextEditor(text: $viewModel.userPrompt)
                            .frame(height: 120)
                            .padding(8)
                            .background(Color(.systemGray6))
                            .cornerRadius(8)
                            .overlay(
                                RoundedRectangle(cornerRadius: 8)
                                    .stroke(Color.gray.opacity(0.3), lineWidth: 1)
                            )
                            .padding(.horizontal)
                            .focused($isTextFieldFocused)
                        
                        Text("Example: \"I want to take portraits in low light\" or \"Landscape photography at sunset\"")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .padding(.horizontal)
                    }
                    .padding(.top)
                    
                    // Get suggestions button
                    Button(action: {
                        isTextFieldFocused = false
                        Task {
                            await viewModel.getSuggestions()
                        }
                    }) {
                        HStack {
                            if viewModel.isLoading {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle())
                            } else {
                                Image(systemName: "sparkles")
                            }
                            Text("Get AI Suggestions")
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(viewModel.userPrompt.isEmpty ? Color.gray : Color.purple)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                    }
                    .disabled(viewModel.userPrompt.isEmpty || viewModel.isLoading)
                    .padding(.horizontal)
                    
                    // Quick prompts
                    VStack(alignment: .leading, spacing: 10) {
                        Text("Quick prompts:")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .padding(.horizontal)
                        
                        ScrollView(.horizontal, showsIndicators: false) {
                            HStack(spacing: 10) {
                                QuickPromptButton(
                                    title: "Portrait",
                                    icon: "person.fill"
                                ) {
                                    viewModel.userPrompt = "Portrait photography with shallow depth of field"
                                }
                                
                                QuickPromptButton(
                                    title: "Landscape",
                                    icon: "mountain.2.fill"
                                ) {
                                    viewModel.userPrompt = "Landscape photography with deep focus"
                                }
                                
                                QuickPromptButton(
                                    title: "Night",
                                    icon: "moon.stars.fill"
                                ) {
                                    viewModel.userPrompt = "Night photography in low light"
                                }
                                
                                QuickPromptButton(
                                    title: "Action",
                                    icon: "figure.run"
                                ) {
                                    viewModel.userPrompt = "Action photography to freeze fast motion"
                                }
                            }
                            .padding(.horizontal)
                        }
                    }
                    
                    // Display suggestions
                    if let suggestions = viewModel.suggestions {
                        VStack(alignment: .leading, spacing: 15) {
                            Divider()
                            
                            SectionHeader(title: "AI Suggestions")
                            
                            if let iso = suggestions.iso {
                                PredictionCard(
                                    icon: "sun.max",
                                    label: "ISO",
                                    value: "\(iso)",
                                    color: .orange
                                )
                            }
                            
                            if let aperture = suggestions.aperture {
                                PredictionCard(
                                    icon: "circle.hexagonpath",
                                    label: "Aperture",
                                    value: aperture,
                                    color: .blue
                                )
                            }
                            
                            if let shutter = suggestions.shutterSpeed {
                                PredictionCard(
                                    icon: "timer",
                                    label: "Shutter Speed",
                                    value: shutter,
                                    color: .green
                                )
                            }
                            
                            if let explanation = suggestions.explanation {
                                VStack(alignment: .leading, spacing: 8) {
                                    HStack {
                                        Image(systemName: "lightbulb.fill")
                                            .foregroundColor(.yellow)
                                        Text("Explanation")
                                            .font(.headline)
                                    }
                                    
                                    Text(explanation)
                                        .font(.body)
                                        .foregroundColor(.primary)
                                }
                                .padding()
                                .background(Color.yellow.opacity(0.1))
                                .cornerRadius(12)
                            }
                            
                            if let source = suggestions.source {
                                Text("Source: \(source)")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                        .padding()
                    }
                    
                    if let error = viewModel.errorMessage {
                        ErrorView(message: error)
                            .padding()
                    }
                    
                    Spacer()
                }
            }
            .navigationTitle("AI Suggestions")
            .toolbar {
                ToolbarItemGroup(placement: .keyboard) {
                    Spacer()
                    Button("Done") {
                        isTextFieldFocused = false
                    }
                }
            }
        }
    }
}

struct QuickPromptButton: View {
    let title: String
    let icon: String
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                Image(systemName: icon)
                    .font(.title2)
                Text(title)
                    .font(.caption)
            }
            .frame(width: 80, height: 80)
            .background(Color.blue.opacity(0.1))
            .cornerRadius(12)
        }
        .buttonStyle(PlainButtonStyle())
    }
}
