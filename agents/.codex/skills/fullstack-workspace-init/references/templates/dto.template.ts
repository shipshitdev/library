/**
 * DTO Templates
 *
 * Replace {{Entity}} with PascalCase entity name (e.g., Task)
 * Replace {{FIELDS}} with actual field definitions
 */

// === create-{{entity}}.dto.ts ===


/**
 * FIELD EXAMPLES - Replace with actual fields:
 *
 * Required string:
 * @IsString()
 * title: string;
 *
 * Optional string:
 * @IsString()
 * @IsOptional()
 * description?: string;
 *
 * Enum:
 * @IsEnum(Priority)
 * @IsOptional()
 * priority?: Priority;
 *
 * Date string:
 * @IsDateString()
 * @IsOptional()
 * dueDate?: string;
 *
 * Boolean:
 * @IsBoolean()
 * @IsOptional()
 * isCompleted?: boolean;
 *
 * Number:
 * @IsNumber()
 * @IsOptional()
 * order?: number;
 *
 * Array of strings:
 * @IsArray()
 * @IsString({ each: true })
 * @IsOptional()
 * tags?: string[];
 */

export class Create{{Entity}}Dto {
  // {{FIELDS}}
}

// === update-{{entity}}.dto.ts ===
{Entity}Dto } from "./create-{{entity}}.dto";

export class Update{{Entity}}Dto extends PartialType(Create{Entity}Dto) {}
