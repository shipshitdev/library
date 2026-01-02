/**
 * NestJS Controller Template
 *
 * Replace {{Entity}} with PascalCase entity name (e.g., Task)
 * Replace {{entity}} with camelCase entity name (e.g., task)
 * Replace {{entities}} with plural camelCase (e.g., tasks)
 */

import {
  Body,
  Controller,
  Delete,
  Get,
  Param,
  Patch,
  Post,
  UseGuards,
} from "@nestjs/common";
import { ApiBearerAuth, ApiOperation, ApiTags } from "@nestjs/swagger";{Entity}sService } from "./{{entities}}.service";{Entity}Dto } from "./dto/create-{{entity}}.dto";{Entity}Dto } from "./dto/update-{{entity}}.dto";

import { CurrentUser } from "../auth/decorators/current-user.decorator";
import { ClerkAuthGuard } from "../auth/guards/clerk-auth.guard";

@ApiTags("{{entities}}")
@ApiBearerAuth()
@UseGuards(ClerkAuthGuard)
@Controller("{{entities}}")
export class {{Entity}}sController {
  constructor(private readonly {{entities}}Service: {{Entity}}sService) 

  @Post()
  @ApiOperation({ summary: "Create a new {{entity}}" })
  create(
    @Body() create{{Entity}}Dto: Create{{Entity}}Dto,
    @CurrentUser() user: { userId: string },
  ) 
    return this.entitiesService.create(create{{Entity}}Dto, user.userId);

  @Get()
  @ApiOperation({ summary: "Get all {{entities}}" })
  findAll(@CurrentUser() user: { userId: string }) 
    return this.entitiesService.findAll(user.userId);

  @Get(":id")
  @ApiOperation({ summary: "Get a {{entity}} by ID" })
  findOne(
    @Param("id") id: string,
    @CurrentUser() user: { userId: string },
  ) 
    return this.entitiesService.findOne(id, user.userId);

  @Patch(":id")
  @ApiOperation({ summary: "Update a {{entity}}" })
  update(
    @Param("id") id: string,
    @Body() update{{Entity}}Dto: Update{{Entity}}Dto,
    @CurrentUser() user: { userId: string },
  ) 
    return this.entitiesService.update(id, update{{Entity}}Dto, user.userId);

  @Delete(":id")
  @ApiOperation({ summary: "Delete a {{entity}}" })
  remove(
    @Param("id") id: string,
    @CurrentUser() user: { userId: string },
  ) 
    return this.entitiesService.remove(id, user.userId);
}
