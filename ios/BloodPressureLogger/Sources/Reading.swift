import Foundation

/// Один вимір тиску: систолічний, діастолічний, пульс і момент часу.
struct Reading: Identifiable, Codable, Equatable {
    var id: UUID = UUID()
    var systolic: Int      // SYS, mmHg
    var diastolic: Int     // DIA, mmHg
    var pulse: Int         // PUL, уд/хв
    var date: Date         // теперішній час на момент збереження

    /// Чи записано цей вимір також у Apple Health.
    var savedToHealth: Bool = false
}

// MARK: - Класифікація тиску (орієнтовно, за категоріями ACC/AHA)

extension Reading {
    enum Category: String {
        case low = "Знижений"
        case normal = "Нормальний"
        case elevated = "Підвищений"
        case stage1 = "Гіпертензія 1 ст."
        case stage2 = "Гіпертензія 2 ст."
        case crisis = "Гіпертонічний криз"

        /// Колір-підказка для інтерфейсу (SwiftUI Color name).
        var tintName: String {
            switch self {
            case .low: return "blue"
            case .normal: return "green"
            case .elevated: return "yellow"
            case .stage1: return "orange"
            case .stage2: return "red"
            case .crisis: return "purple"
            }
        }
    }

    /// Проста категоризація за систолічним/діастолічним.
    /// Це НЕ медична порада — лише візуальна підказка.
    var category: Category {
        if systolic >= 180 || diastolic >= 120 { return .crisis }
        if systolic >= 140 || diastolic >= 90 { return .stage2 }
        if systolic >= 130 || diastolic >= 80 { return .stage1 }
        if systolic >= 120 && diastolic < 80 { return .elevated }
        if systolic < 90 || diastolic < 60 { return .low }
        return .normal
    }
}
