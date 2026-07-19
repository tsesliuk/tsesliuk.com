import Foundation
import Vision
import UIKit

/// Результат розпізнавання з фото. Будь-яке поле може бути nil,
/// якщо OCR не знайшов правдоподібного числа.
struct RecognizedReading {
    var systolic: Int?
    var diastolic: Int?
    var pulse: Int?
}

/// Розпізнавання показників тиску з фотографії — повністю на пристрої
/// через фреймворк Vision. Нічого нікуди не надсилається.
enum TextRecognizer {

    /// Знаходить числа на зображенні й розкладає їх на SYS/DIA/PUL за
    /// вертикальним положенням (зверху вниз, як на дисплеї тонометра).
    static func recognize(from image: UIImage) async -> RecognizedReading {
        guard let cgImage = image.cgImage else { return RecognizedReading() }

        return await withCheckedContinuation { continuation in
            let request = VNRecognizeTextRequest { request, _ in
                let observations = (request.results as? [VNRecognizedTextObservation]) ?? []

                // Збираємо (вертикальна позиція, число) для правдоподібних значень.
                // Vision має початок координат унизу ліворуч, тож більший midY = вище.
                var numbers: [(y: CGFloat, value: Int)] = []
                for observation in observations {
                    guard let text = observation.topCandidates(1).first?.string else { continue }
                    for token in Self.integerTokens(in: text) where (30...260).contains(token) {
                        numbers.append((observation.boundingBox.midY, token))
                    }
                }

                numbers.sort { $0.y > $1.y } // зверху вниз

                var result = RecognizedReading()
                if numbers.indices.contains(0) { result.systolic = numbers[0].value }
                if numbers.indices.contains(1) { result.diastolic = numbers[1].value }
                if numbers.indices.contains(2) { result.pulse = numbers[2].value }
                continuation.resume(returning: result)
            }
            request.recognitionLevel = .accurate
            request.usesLanguageCorrection = false

            let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
            DispatchQueue.global(qos: .userInitiated).async {
                try? handler.perform([request])
            }
        }
    }

    /// Витягує цілі числа з рядка (напр. "134" з "134", "18" з "0:18").
    private static func integerTokens(in text: String) -> [Int] {
        text
            .components(separatedBy: CharacterSet(charactersIn: "0123456789").inverted)
            .compactMap { $0.isEmpty ? nil : Int($0) }
    }
}
