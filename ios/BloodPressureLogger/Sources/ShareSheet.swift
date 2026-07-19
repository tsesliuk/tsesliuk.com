import SwiftUI
import UIKit

/// Обгортка над системним аркушем «Поділитися» (UIActivityViewController).
struct ShareSheet: UIViewControllerRepresentable {
    let items: [Any]

    func makeUIViewController(context: Context) -> UIActivityViewController {
        UIActivityViewController(activityItems: items, applicationActivities: nil)
    }

    func updateUIViewController(_ controller: UIActivityViewController, context: Context) {}
}

/// Ідентифікований файл для показу через `.sheet(item:)`.
struct ExportFile: Identifiable {
    let id = UUID()
    let url: URL
}
