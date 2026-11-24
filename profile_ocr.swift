import AppKit
import PDFKit
import Vision

func recognize(_ image: NSImage) throws -> String {
    var bounds = CGRect(origin: .zero, size: image.size)
    guard let pixels = image.cgImage(forProposedRect: &bounds, context: nil, hints: nil) else {
        throw CocoaError(.fileReadCorruptFile)
    }
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    try VNImageRequestHandler(cgImage: pixels).perform([request])
    return (request.results ?? []).compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
}

let url = URL(fileURLWithPath: CommandLine.arguments[1])
do {
    if url.pathExtension.lowercased() == "pdf" {
        guard let pdf = PDFDocument(url: url), !pdf.isLocked else {
            throw CocoaError(.fileReadCorruptFile)
        }
        if pdf.pageCount > 40 {
            fputs("Import PDFs with up to 40 pages.\n", stderr)
            exit(1)
        }
        for index in 0..<pdf.pageCount {
            guard let page = pdf.page(at: index) else { continue }
            let text = page.string?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
            if text.isEmpty {
                print(try recognize(page.thumbnail(of: CGSize(width: 1600, height: 2000), for: .mediaBox)))
            } else {
                print(text)
            }
        }
    } else {
        guard let image = NSImage(contentsOf: url) else { throw CocoaError(.fileReadCorruptFile) }
        print(try recognize(image))
    }
} catch {
    fputs("Could not read the PDF or image.\n", stderr)
    exit(1)
}
