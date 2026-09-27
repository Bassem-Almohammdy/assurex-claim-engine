export type ClaimStatus = 'Valid' | 'Invalid' | 'Manual Review' | 'Pending';
export type WarrantyStatus = 'Active' | 'Expiring' | 'Expired';
export type RuleStatus = 'Passed' | 'Warning' | 'Failed';
export type FinalDecision = 'Likely Valid' | 'Likely Invalid' | 'Manual Review Required';
export type PredictionLabel = 'Valid' | 'Invalid' | 'Manual Review';

export interface Product {
  id: string;
  name: string;
  category: string;
  brand: string;
  modelNumber: string;
  serialNumber: string;
  purchaseDate: string;
  purchasePrice: number;
  warrantyDurationMonths: number;
  image?: string;
}

export interface Warranty {
  id: string;
  productId: string;
  productName: string;
  status: WarrantyStatus;
  startDate: string;
  endDate: string;
  durationMonths: number;
  daysRemaining: number;
}

export interface DocumentItem {
  id: string;
  name: string;
  type: 'Purchase Receipt' | 'Warranty Card' | 'Product Image' | 'Serial Number Evidence' | 'Fault Evidence' | 'Repair Report';
  fileType: 'image' | 'pdf';
  fileSize: string;
  uploadStatus: 'Uploaded' | 'Pending' | 'Failed';
  uploadedAt: string;
}

export interface PredictionResult {
  model: 'Python Classification Model' | 'Google Teachable Machine';
  prediction: PredictionLabel;
  validConfidence: number;
  invalidConfidence: number;
  manualReviewConfidence: number;
}

export interface WarrantyRule {
  id: string;
  name: string;
  status: RuleStatus;
  message: string;
}

export interface ModelComparison {
  pythonPrediction: PredictionLabel;
  tmPrediction: PredictionLabel;
  predictionMatch: boolean;
  confidenceDifference: number;
  modelConsistency: 'Strong Match' | 'Moderate Match' | 'Mismatch';
}

export interface ContradictionItem {
  id: string;
  description: string;
  severity: 'High' | 'Medium' | 'Low';
}

export interface ClaimSummary {
  claimId: string;
  product: string;
  productCategory: string;
  productAge: string;
  warrantyPeriod: string;
  warrantyStatus: WarrantyStatus;
  faultType: string;
  repairHistory: string;
  receiptAvailable: boolean;
  serialNumberStatus: 'Verified' | 'Unverified' | 'Mismatch';
  missingDocuments: string[];
}

export interface Claim {
  id: string;
  productId: string;
  product: string;
  productCategory: string;
  customer: string;
  customerEmail: string;
  status: ClaimStatus;
  warrantyStatus: WarrantyStatus;
  submittedDate: string;
  faultOccurrenceDate: string;
  faultDescription: string;
  damageType: string;
  previousRepairs: string;
  serviceCenter: string;
  brand: string;
  modelNumber: string;
  serialNumber: string;
  purchaseDate: string;
  purchasePrice: number;
  warrantyDurationMonths: number;
  documents: DocumentItem[];
  summary: ClaimSummary;
  pythonPrediction: PredictionResult;
  tmPrediction: PredictionResult;
  comparison: ModelComparison;
  rules: WarrantyRule[];
  contradictions: ContradictionItem[];
  duplicateStatus: string;
  finalDecision: FinalDecision;
}
