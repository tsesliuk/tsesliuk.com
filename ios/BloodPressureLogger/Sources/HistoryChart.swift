import SwiftUI
import Charts

/// Графік динаміки: систолічний і діастолічний тиск у часі.
struct HistoryChart: View {
    let readings: [Reading]

    // Для лінії потрібен хронологічний порядок (сховище тримає новіші зверху).
    private var chronological: [Reading] {
        readings.sorted { $0.date < $1.date }
    }

    var body: some View {
        Chart {
            ForEach(chronological) { reading in
                LineMark(
                    x: .value("Час", reading.date),
                    y: .value("mmHg", reading.systolic),
                    series: .value("Показник", "Систолічний")
                )
                .foregroundStyle(by: .value("Показник", "Систолічний"))
                .symbol(.circle)

                LineMark(
                    x: .value("Час", reading.date),
                    y: .value("mmHg", reading.diastolic),
                    series: .value("Показник", "Діастолічний")
                )
                .foregroundStyle(by: .value("Показник", "Діастолічний"))
                .symbol(.circle)
            }
        }
        .chartForegroundStyleScale([
            "Систолічний": Color.red,
            "Діастолічний": Color.blue
        ])
        .chartYScale(domain: .automatic(includesZero: false))
        .chartLegend(position: .bottom)
        .frame(height: 200)
        .padding(.vertical, 4)
    }
}
