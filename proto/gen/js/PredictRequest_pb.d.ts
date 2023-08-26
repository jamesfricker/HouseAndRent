// package: 
// file: PredictRequest.proto

import * as jspb from "google-protobuf";

export class PredictRequest extends jspb.Message {
  getCity(): string;
  setCity(value: string): void;

  getSuburb(): string;
  setSuburb(value: string): void;

  getHouseType(): string;
  setHouseType(value: string): void;

  getBedroomCount(): number;
  setBedroomCount(value: number): void;

  getBathroomCount(): number;
  setBathroomCount(value: number): void;

  getPriceIncludesBills(): boolean;
  setPriceIncludesBills(value: boolean): void;

  getRoomsAvailable(): number;
  setRoomsAvailable(value: number): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): PredictRequest.AsObject;
  static toObject(includeInstance: boolean, msg: PredictRequest): PredictRequest.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: PredictRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): PredictRequest;
  static deserializeBinaryFromReader(message: PredictRequest, reader: jspb.BinaryReader): PredictRequest;
}

export namespace PredictRequest {
  export type AsObject = {
    city: string,
    suburb: string,
    houseType: string,
    bedroomCount: number,
    bathroomCount: number,
    priceIncludesBills: boolean,
    roomsAvailable: number,
  }
}

export class PredictResponse extends jspb.Message {
  getPrediction(): number;
  setPrediction(value: number): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): PredictResponse.AsObject;
  static toObject(includeInstance: boolean, msg: PredictResponse): PredictResponse.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: PredictResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): PredictResponse;
  static deserializeBinaryFromReader(message: PredictResponse, reader: jspb.BinaryReader): PredictResponse;
}

export namespace PredictResponse {
  export type AsObject = {
    prediction: number,
  }
}

